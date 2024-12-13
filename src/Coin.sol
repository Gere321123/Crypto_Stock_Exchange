// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Import OpenZeppelin's ERC20 implementation
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract Coin is ERC20, Ownable, ReentrancyGuard {
    error Coin__MustBeMoreThanZero();
    error Coin__NotEnoughTokensAvailable();
    error Coin__InsufficientTokens();
    error Coin__NotAuthorized();
    error Coin__CompanyWantsToWithdrawMoreMoneyThanAllowed();
    error Coin__BurnMoreThanTheTokensInTheMarcatCap();
    error Coin__InsufficientWBTC();
    error Coin__WBTCTransferFailed();
    error Coin__FailedToSendWBTC();
    error Coin__InsufficientWBTCInContract();
    error Coin__FailedToReceiveWBTC();

    event TokensBought(address indexed buyer, uint256 wBTCAmount, uint256 tokenAmount);
    event TokensSold(address indexed seller, uint256 tokenAmount, uint256 wBTCAmount);
    event Withdrawal(address indexed account, uint256 amount);

    IERC20 public constant wBTC = IERC20(0x5FC8d32690cc91D4c39d9d3abcBD16989F875707); //This wrapper Bitcoin address is for Etherium network : 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599

    address private immutable i_owner;
    uint8 private immutable i_OWNERWITHDRAWALPERCENTAGE;
    uint256 private ownerAllreadyWithdrawalThisMany = 0;
    address private immutable i_secondowner;
    uint8 private immutable i_SECONDOWNERWITHDRAWALPERCENTAGE;
    uint256 private secondownerAllreadyWithdrawalThisMany = 0;

    uint256 private valueOfOneTokenInWei;
    int256 private numberOfVirtualWei;
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
    ) ERC20("CryptoStock", "CS") Ownable(address(this)) {
        i_owner = msg.sender;

        i_company = _company;
        companyWithdrawalPercentage = _companyWithdrawalPercentage;
        i_SECONDOWNERWITHDRAWALPERCENTAGE = _i_SECONDOWNERWITHDRAWALPERCENTAGE;
        i_OWNERWITHDRAWALPERCENTAGE = _i_OWNERWITHDRAWALPERCENTAGE;
        i_secondowner = _i_secondowner;
        numberOfVirtualWei = int256(_i_numberOfVirtualWei);

        _mint(address(this), _numberOfTokens * (10 ** decimals()));

        valueOfOneTokenInWei = _i_numberOfVirtualWei * (10 ** decimals()) / totalSupply();
        i_formulaConstans = _i_numberOfVirtualWei * totalSupply();
    }

    // Modifier to check if the caller is the company
    modifier onlyCompany() {
        if (msg.sender != i_company) {
            revert Coin__NotAuthorized();
        }
        _;
    }
    // Only the owner or the secendOwner or the company

    modifier onlyAuthorized() {
        if (!(msg.sender == i_owner || msg.sender == i_secondowner || msg.sender == i_company)) {
            revert Coin__NotAuthorized();
        }
        _;
    }

    modifier wBitMoreThenZeroAndTheSenderHaveEnough(uint256 wBTCAmount) {
        if (wBTCAmount < 0) {
            revert Coin__MustBeMoreThanZero();
        }

        uint256 senderWBTCBalance = wBTC.balanceOf(msg.sender);
        if (senderWBTCBalance < wBTCAmount) {
            revert Coin__InsufficientWBTC();
        }
        _;
    }

    function buyTokens(uint256 wBTCAmount) external nonReentrant wBitMoreThenZeroAndTheSenderHaveEnough(wBTCAmount) {
        uint256 numberOfTokensAffterBuy;
        uint256 liqviditywBTCAmount = wBTCAmount - (wBTCAmount / 10000);

        if (numberOfVirtualWei >= 0) {
            numberOfTokensAffterBuy =
                i_formulaConstans / (getwBTCBalance() + uint256(numberOfVirtualWei) + liqviditywBTCAmount);
        } else {
            uint256 adjustedBalance = getwBTCBalance() - uint256(-numberOfVirtualWei) + liqviditywBTCAmount;
            numberOfTokensAffterBuy = i_formulaConstans / adjustedBalance;
        }

        uint256 tokensToBuy = totalSupply() - numberOfTokensInTheMarcetCap - numberOfTokensAffterBuy;

        if (tokensToBuy > balanceOf(address(this))) {
            revert Coin__NotEnoughTokensAvailable();
        }

        uint256 allowance = wBTC.allowance(msg.sender, address(this));
        if (allowance < wBTCAmount) {
            revert ERC20InsufficientAllowance(msg.sender, allowance, wBTCAmount);
        }

        // Transfer wBTC from buyer to the contract
        bool success = wBTC.transferFrom(msg.sender, address(this), wBTCAmount);
        if (!success) {
            revert Coin__WBTCTransferFailed();
        }

        // Transfer tokens to the buyer
        _transfer(address(this), msg.sender, tokensToBuy);
        numberOfTokensInTheMarcetCap += tokensToBuy;

        adjustPrice();

        emit TokensBought(msg.sender, wBTCAmount, tokensToBuy);
    }

    function sellTokens(uint256 _tokenAmount) public nonReentrant {
        if (_tokenAmount <= 0) {
            revert Coin__MustBeMoreThanZero();
        }

        uint256 userBalance = balanceOf(msg.sender);
        if (userBalance < _tokenAmount) {
            revert Coin__InsufficientTokens();
        }
        uint256 contractwBTCBalance = getwBTCBalance();

        // Calculate the amount of wBTC to return
        uint256 numberOfWeiAfterSell = i_formulaConstans / (totalSupply() - numberOfTokensInTheMarcetCap + _tokenAmount);
        uint256 wBTCAmountToReturn;
        if (numberOfVirtualWei >= 0) {
            // If numberOfVirtualWei is positive, add it directly
            wBTCAmountToReturn = contractwBTCBalance + uint256(numberOfVirtualWei) - numberOfWeiAfterSell;
        } else {
            // If numberOfVirtualWei is negative, subtract its absolute value
            uint256 adjustedBalance = contractwBTCBalance - uint256(-numberOfVirtualWei);
            wBTCAmountToReturn = adjustedBalance - numberOfWeiAfterSell;
        }

        // Check if the contract has enough wBTC
        if (contractwBTCBalance < wBTCAmountToReturn) {
            revert Coin__InsufficientWBTCInContract();
        }

        // Transfer the tokens from the seller to the contract
        _transfer(msg.sender, address(this), _tokenAmount);

        // Transfer wBTC to the seller
        bool success = wBTC.transfer(msg.sender, wBTCAmountToReturn);
        if (!success) {
            revert Coin__FailedToSendWBTC();
        }

        // Adjust the market cap and price
        numberOfTokensInTheMarcetCap -= _tokenAmount;

        adjustPrice();

        emit TokensSold(msg.sender, _tokenAmount, wBTCAmountToReturn);
    }

    function adjustPrice() internal {
        uint256 adjustedBalance;

        if (numberOfVirtualWei >= 0) {
            adjustedBalance = getwBTCBalance() + uint256(numberOfVirtualWei);
        } else {
            adjustedBalance = getwBTCBalance() - uint256(-numberOfVirtualWei);
        }
        valueOfOneTokenInWei = adjustedBalance * (10 ** decimals()) / (totalSupply() - numberOfTokensInTheMarcetCap);
    }

    // Withdraw BIT function for the company
    function withdrawCompany(uint256 withdrawValueinWei) external onlyCompany {
        if (companyCanWithdraw) {
            withdrawMoney(withdrawValueinWei, companyAllreadyWithdrawalThisMany, companyWithdrawalPercentage, i_company);
            companyAllreadyWithdrawalThisMany += int256(withdrawValueinWei);
            emit Withdrawal(msg.sender, withdrawValueinWei);
        }
    }

    function uplodeMoney(uint256 wBTCAmount)
        external
        onlyCompany
        nonReentrant
        wBitMoreThenZeroAndTheSenderHaveEnough(wBTCAmount)
    {
        // Transfer wBTC from the caller to the contract
        bool success = wBTC.transferFrom(msg.sender, address(this), wBTCAmount);
        if (!success) {
            revert Coin__FailedToReceiveWBTC();
        }

        uint256 bitBalance = getwBTCBalanceNotZero();

        // Calculate tokens after the burn
        uint256 tokensAfterBurn;
        if (numberOfVirtualWei >= 0) {
            tokensAfterBurn = bitBalance + uint256(numberOfVirtualWei);
        } else {
            tokensAfterBurn = bitBalance - uint256(-numberOfVirtualWei);
        }

        // Burn excess tokens
        burn(totalSupply() - numberOfTokensInTheMarcetCap - tokensAfterBurn);

        // Adjust numberOfVirtualWei based on the wBTC uploaded
        numberOfVirtualWei += (numberOfVirtualWei * int256(wBTCAmount)) / int256(bitBalance - wBTCAmount);

        // Update company withdrawal tracker
        companyAllreadyWithdrawalThisMany -= int256(wBTCAmount);

        // Adjust the token price
        adjustPrice();
    }

    function changePrice(uint256 valueinWei) internal {
        uint256 bitBalance = getwBTCBalanceNotZero();

        uint256 tokensAfterMint;

        if (numberOfVirtualWei >= 0) {
            tokensAfterMint = i_formulaConstans / (bitBalance + uint256(numberOfVirtualWei));
        } else {
            tokensAfterMint = i_formulaConstans / (bitBalance - uint256(-numberOfVirtualWei));
        }

        uint256 numberOfMint;
        numberOfMint = tokensAfterMint - (totalSupply() - numberOfTokensInTheMarcetCap);
        mint(numberOfMint);

        int256 burnVirtualBit = (int256(valueinWei) * numberOfVirtualWei) / int256(bitBalance + valueinWei);
        if (burnVirtualBit < 0) {
            numberOfVirtualWei += burnVirtualBit;
        } else {
            numberOfVirtualWei -= burnVirtualBit;
        }
        adjustPrice();
    }

    function withdowOwners(uint256 withdrawValueinWei) external {
        if (msg.sender == i_owner) {
            withdrawMoney(
                withdrawValueinWei, int256(ownerAllreadyWithdrawalThisMany), i_OWNERWITHDRAWALPERCENTAGE, i_owner
            );
            ownerAllreadyWithdrawalThisMany += withdrawValueinWei;
            emit Withdrawal(msg.sender, withdrawValueinWei);
        } else {
            if (msg.sender == i_secondowner) {
                withdrawMoney(
                    withdrawValueinWei,
                    int256(secondownerAllreadyWithdrawalThisMany),
                    i_SECONDOWNERWITHDRAWALPERCENTAGE,
                    i_secondowner
                );
                secondownerAllreadyWithdrawalThisMany += withdrawValueinWei;
                emit Withdrawal(msg.sender, withdrawValueinWei);
            } else {
                revert Coin__NotAuthorized();
            }
        }
    }

    function withdrawMoney(
        uint256 withdrawValueInWBTC,
        int256 alreadyWithdrawnThisMany,
        uint256 withdrawalPercentage,
        address _to
    ) internal nonReentrant {
        // Get the contract's wBTC balance
        int256 wBTCBalance = int256(getwBTCBalance());

        // Calculate the maximum withdrawal allowed based on the percentage
        int256 maxWithdrawal = (wBTCBalance * int256(withdrawalPercentage)) / 100;

        // Revert if the requested withdrawal exceeds the allowed percentage
        if (int256(withdrawValueInWBTC) + alreadyWithdrawnThisMany > maxWithdrawal) {
            revert Coin__InsufficientWBTCInContract();
        }

        // Transfer wBTC to the specified address
        bool success = wBTC.transfer(_to, withdrawValueInWBTC);
        if (!success) {
            revert Coin__FailedToSendWBTC();
        }

        // Adjust the price or perform other necessary updates
        changePrice(withdrawValueInWBTC);
    }

    function getwBTCBalance() public view returns (uint256) {
        return wBTC.balanceOf(address(this));
    }

    function getwBTCBalanceNotZero() public view returns (uint256) {
        uint256 balance = getwBTCBalance();
        if (balance <= 0) {
            revert Coin__MustBeMoreThanZero();
        }
        return balance;
    }

    function setcompanyWithdrawalPercentage(uint8 newcompanyWithdrawalPercentage) external onlyOwner {
        if (newcompanyWithdrawalPercentage + i_OWNERWITHDRAWALPERCENTAGE + i_SECONDOWNERWITHDRAWALPERCENTAGE < 100) {
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

    function getMarketCap() public view returns (uint256) {
        return numberOfTokensInTheMarcetCap * valueOfOneTokenInWei;
    }

    function geNumberOfTokensInTheMarcetCapp() public view returns (uint256) {
        return numberOfTokensInTheMarcetCap;
    }

    function getValueOfOneTokenInWei() public view returns (uint256) {
        return valueOfOneTokenInWei;
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
