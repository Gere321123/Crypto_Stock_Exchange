// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Import OpenZeppelin's ERC20 implementation
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {console} from "forge-std/console.sol";

contract Coin is ERC20, Ownable, ReentrancyGuard {
    error Coin__MustBeMoreThanZero();
    error Coin__NotEnoughTokensAvailable();
    error Coin__InsufficientTokens();
    error Coin__InsufficientETHInContract();
    error Coin__FailedToSendETH();
    error Coin__NotAuthorized();
    error Coin__CompanyWantsToWithdrawMoreMoneyThanAllowed();
    error Coin__BurnMoreThanTheTokensInTheMarcatCap();
    error Coin__ethBalanceMustBeMoreThanZero();

    address private immutable i_owner;
    uint8 private oWNERWITHDRAWALPERCENTAGE;
    uint256 private ownerAllreadyWithdrawalThisMany = 0;
    address private immutable i_secondowner;
    uint8 private immutable i_SECONDOWNERWITHDRAWALPERCENTAGE;
    uint256 private secondownerAllreadyWithdrawalThisMany = 0;

    uint256 private valueOfOneTokenInWei;
    uint256 private numberOfVirtualWei;
    uint256 private immutable i_formulaConstans;

    address private immutable i_company;
    uint8 private companyWithdrawalPercentage = 20;
    int256 private companyAllreadyWithdrawalThisMany = 0;
    uint256 private numberOfTokensInTheMarcetCap = 0;

    bool private companyCanWithdraw = true;

    constructor(
        uint256 _numberOfTokens,
        address _company,
        uint8 _companyWithdrawalPercentage,
        uint8 _i_OWNERWITHDRAWALPERCENTAGE,
        uint8 _i_SECONDOWNERWITHDRAWALPERCENTAGE,
        address _i_secondowner,
        uint256 _i_numberOfVirtualWei
    ) ERC20("FixedSupplyCoin", "FSC") Ownable(address(this)) {
        i_owner = msg.sender;

        i_company = _company;
        companyWithdrawalPercentage = _companyWithdrawalPercentage;
        i_SECONDOWNERWITHDRAWALPERCENTAGE = _i_SECONDOWNERWITHDRAWALPERCENTAGE;
        oWNERWITHDRAWALPERCENTAGE = _i_OWNERWITHDRAWALPERCENTAGE;
        i_secondowner = _i_secondowner;
        numberOfVirtualWei = _i_numberOfVirtualWei;

        _mint(address(this), _numberOfTokens * (10 ** decimals()));

        valueOfOneTokenInWei = numberOfVirtualWei * (10 ** decimals()) / totalSupply();
        i_formulaConstans = numberOfVirtualWei * totalSupply();
    }

    // Modifier to check if the caller is the company
    modifier onlyCompany() {
        if (msg.sender != i_company) {
            revert Coin__NotAuthorized();
        }
        _;
    }

    modifier onlyAuthorized() {
        if (!(msg.sender == i_owner || msg.sender == i_secondowner || msg.sender == i_company)) {
            revert Coin__NotAuthorized();
        }
        _;
    }

    function buyTokens() external payable nonReentrant {
        if (msg.value < 0) {
            revert Coin__MustBeMoreThanZero();
        }

        uint256 numberOfTokensAffterBuy = i_formulaConstans / (getethBalance() + numberOfVirtualWei);
        uint256 tokensToBuy = totalSupply() - numberOfTokensInTheMarcetCap - numberOfTokensAffterBuy;
        if (tokensToBuy > balanceOf(address(this))) {
            revert Coin__NotEnoughTokensAvailable();
        }

        // Transfer tokens to the buyer
        _transfer(address(this), msg.sender, tokensToBuy);
        numberOfTokensInTheMarcetCap += tokensToBuy;
        adjustPrice();
    }

    function sellTokens(uint256 _tokenAmount) public nonReentrant {
        if (_tokenAmount <= 0) {
            revert Coin__MustBeMoreThanZero();
        }
        uint256 userBalance = balanceOf(msg.sender);
        if (userBalance < _tokenAmount) {
            revert Coin__InsufficientTokens();
        }

        uint256 numberOfWeiAffterBuy = i_formulaConstans / (totalSupply() - numberOfTokensInTheMarcetCap + _tokenAmount);
        uint256 weitAmountToReturn = getethBalance() + numberOfVirtualWei - numberOfWeiAffterBuy;

        if (address(this).balance < weitAmountToReturn) {
            revert Coin__InsufficientETHInContract();
        }

        // Adjust the price based on sell

        // Transfer the tokens from the seller to the contract
        _transfer(msg.sender, address(this), _tokenAmount);

        // Send ETH to the seller
        (bool sent,) = msg.sender.call{value: weitAmountToReturn}("");
        if (!sent) {
            revert Coin__FailedToSendETH();
        }
        numberOfTokensInTheMarcetCap -= _tokenAmount;

        adjustPrice();
    }

    function adjustPrice() internal {
        valueOfOneTokenInWei =
            (numberOfVirtualWei + getethBalance()) * (10 ** decimals()) / (totalSupply() - numberOfTokensInTheMarcetCap);
    }

    // Withdraw ETH function for the company
    function withdrawCompany(uint256 withdrawValueinWei) external onlyCompany {
        if (companyCanWithdraw) {
            withdrowMoney(withdrawValueinWei, companyAllreadyWithdrawalThisMany, companyWithdrawalPercentage, i_company);
            companyAllreadyWithdrawalThisMany += int256(withdrawValueinWei);
        }
    }

    function uplodeMoney() external payable onlyCompany nonReentrant {
        if (msg.value < 0) {
            revert Coin__MustBeMoreThanZero();
        }

        uint256 ethBalance = getethBalanceNotZero();

        uint256 tokensAfftherBurn = i_formulaConstans / (ethBalance + numberOfVirtualWei);
        burn(totalSupply() - numberOfTokensInTheMarcetCap - tokensAfftherBurn);

        numberOfVirtualWei += (msg.value * numberOfVirtualWei) / (ethBalance - msg.value);

        companyAllreadyWithdrawalThisMany -= int256(msg.value);
        adjustPrice();
    }

    function cahngePrice(uint256 valueinWei) internal {
        uint256 ethBalance = getethBalanceNotZero();

        uint256 tokensAfftherMint = i_formulaConstans / (ethBalance + numberOfVirtualWei);
        uint256 numberOfmint = tokensAfftherMint - (totalSupply() - numberOfTokensInTheMarcetCap);
        mint(numberOfmint);

        uint256 burnVirtualEth = (valueinWei * numberOfVirtualWei) / (ethBalance + valueinWei);
        numberOfVirtualWei -= burnVirtualEth;
        adjustPrice();
    }

    function withdowOwners(uint256 withdrawValueinWei) external {
        if (msg.sender == i_owner) {
            withdrowMoney(
                withdrawValueinWei, int256(ownerAllreadyWithdrawalThisMany), oWNERWITHDRAWALPERCENTAGE, i_owner
            );
            ownerAllreadyWithdrawalThisMany += withdrawValueinWei;
        } else {
            if (msg.sender == i_secondowner) {
                withdrowMoney(
                    withdrawValueinWei,
                    int256(secondownerAllreadyWithdrawalThisMany),
                    i_SECONDOWNERWITHDRAWALPERCENTAGE,
                    i_secondowner
                );
                secondownerAllreadyWithdrawalThisMany += withdrawValueinWei;
            } else {
                revert Coin__NotAuthorized();
            }
        }
    }

    function withdrowMoney(
        uint256 withdrawValueinWei,
        int256 allreadyWithdrawalThisMany,
        uint256 withdrawalPercentage,
        address _to
    ) internal nonReentrant {
        int256 ethBalance = int256(getethBalance());
        int256 maxWithdrawal = ethBalance * int256(withdrawalPercentage) / 100;

        // Revert if the requested withdrawal exceeds the 20% limit
        if (int256(withdrawValueinWei) + allreadyWithdrawalThisMany > maxWithdrawal) {
            revert Coin__InsufficientETHInContract();
        }

        // Send the requested value to the company
        (bool success,) = payable(_to).call{value: withdrawValueinWei}("");
        if (!success) {
            revert Coin__InsufficientETHInContract();
        }

        cahngePrice(withdrawValueinWei);
    }

    function getethBalance() public view returns (uint256) {
        uint256 ethBalance = address(this).balance;
        if (ethBalance < 0) {
            revert Coin__InsufficientETHInContract();
        }
        return ethBalance;
    }

    function getethBalanceNotZero() public view returns (uint256) {
        uint256 ethBalance = address(this).balance;
        if (ethBalance <= 0) {
            revert Coin__MustBeMoreThanZero();
        }
        return ethBalance;
    }

    function setcompanyWithdrawalPercentage(uint8 newcompanyWithdrawalPercentage) external onlyOwner {
        if (newcompanyWithdrawalPercentage + oWNERWITHDRAWALPERCENTAGE + i_SECONDOWNERWITHDRAWALPERCENTAGE < 100) {
            companyWithdrawalPercentage = newcompanyWithdrawalPercentage;
        } else {
            revert Coin__CompanyWantsToWithdrawMoreMoneyThanAllowed();
        }
    }

    function mint(uint256 _numberOfTokens) public onlyAuthorized {
        if (_numberOfTokens <= 0) {
            revert Coin__MustBeMoreThanZero();
        }
        _mint(address(this), _numberOfTokens);
    }

    function burn(uint256 _numberOfTokens) public onlyAuthorized {
        if (_numberOfTokens <= 0) {
            revert Coin__MustBeMoreThanZero();
        }
        if (_numberOfTokens > totalSupply() - numberOfTokensInTheMarcetCap) {
            revert Coin__BurnMoreThanTheTokensInTheMarcatCap();
        }
        _burn(address(this), _numberOfTokens);
    }

    function setCompanyCanWithdraw(bool _companyCanWithdraw) external onlyOwner {
        companyCanWithdraw = _companyCanWithdraw;
    }

    function setoWNERWITHDRAWALPERCENTAGE(uint8 _oWNERWITHDRAWALPERCENTAGE) external onlyOwner {
        if (companyWithdrawalPercentage + _oWNERWITHDRAWALPERCENTAGE + i_SECONDOWNERWITHDRAWALPERCENTAGE < 100) {
            oWNERWITHDRAWALPERCENTAGE = _oWNERWITHDRAWALPERCENTAGE;
        }
    }

    function getMarketCap() public view returns (uint256) {
        return numberOfTokensInTheMarcetCap * valueOfOneTokenInWei;
    }

    function geNumberOfTokensInTheMarcetCapp() public view returns (uint256) {
        return numberOfTokensInTheMarcetCap;
    }

    function getValueOfOneTokenInWei() public view returns (uint256) {
        return valueOfOneTokenInWei;
    }

    function getContractWeiBalance() public view returns (uint256) {
        return address(this).balance;
    }

    function getownerAllreadyWithdrawalThisMany() public view returns (uint256) {
        return ownerAllreadyWithdrawalThisMany;
    }

    function getsecondownerAllreadyWithdrawalThisMany() public view returns (uint256) {
        return secondownerAllreadyWithdrawalThisMany;
    }

    function getcompanyWithdrawalPercentage() public view returns (uint256) {
        return companyWithdrawalPercentage;
    }

    function getcompanyAllreadyWithdrawalThisMany() public view returns (int256) {
        return companyAllreadyWithdrawalThisMany;
    }
}
