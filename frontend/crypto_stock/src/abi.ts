export const abi = [
  {
    type: 'function',
    name: 'buyTokens',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'wBTCAmount', type: 'uint256' }
    ],
    outputs: []
  },
  {
    type: 'function',
    name: 'sellTokens',
    stateMutability: 'nonpayable',
    inputs: [
      { name: '_tokenAmount', type: 'uint256' }
    ],
    outputs: []
  },
  {
    type: 'function',
    name: 'withdrawCompany',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'withdrawValueinWei', type: 'uint256' }
    ],
    outputs: []
  },
  {
    type: 'function',
    name: 'uplodeMoney',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'wBTCAmount', type: 'uint256' }
    ],
    outputs: []
  },
  {
    type: 'function',
    name: 'changePrice',
    stateMutability: 'internal',
    inputs: [
      { name: 'valueinWei', type: 'uint256' }
    ],
    outputs: []
  },
  {
    type: 'function',
    name: 'withdowOwners',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'withdrawValueinWei', type: 'uint256' }
    ],
    outputs: []
  },
  {
    type: 'function',
    name: 'setcompanyWithdrawalPercentage',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'newcompanyWithdrawalPercentage', type: 'uint8' }
    ],
    outputs: []
  },
  {
    type: 'function',
    name: 'setCompanyCanWithdraw',
    stateMutability: 'nonpayable',
    inputs: [
      { name: '_companyCanWithdraw', type: 'bool' }
    ],
    outputs: []
  },
  {
    type: 'function',
    name: 'getMarketCap',
    stateMutability: 'view',
    inputs: [],
    outputs: [
      { name: '', type: 'uint256' }
    ]
  },
  {
    type: 'function',
    name: 'geNumberOfTokensInTheMarcetCapp',
    stateMutability: 'view',
    inputs: [],
    outputs: [
      { name: '', type: 'uint256' }
    ]
  },
  {
    type: 'function',
    name: 'getValueOfOneTokenInWei',
    stateMutability: 'view',
    inputs: [],
    outputs: [
      { name: '', type: 'uint256' }
    ]
  },
  {
    type: 'function',
    name: 'getwBTCBalance',
    stateMutability: 'view',
    inputs: [],
    outputs: [
      { name: '', type: 'uint256' }
    ]
  },
  {
    type: 'function',
    name: 'getwBTCBalanceNotZero',
    stateMutability: 'view',
    inputs: [],
    outputs: [
      { name: '', type: 'uint256' }
    ]
  },
  {
    type: 'function',
    name: 'setcompanyWithdrawalPercentage',
    stateMutability: 'nonpayable',
    inputs: [
      { name: 'newcompanyWithdrawalPercentage', type: 'uint8' }
    ],
    outputs: []
  },
  {
    type: 'function',
    name: 'balanceOf',
    stateMutability: 'view',
    inputs: [{ name: 'account', type: 'address' }],
    outputs: [{ type: 'uint256' }],
  },
  {
    type: 'function',
    name: 'totalSupply',
    stateMutability: 'view',
    inputs: [],
    outputs: [{ name: 'supply', type: 'uint256' }],
  },
] as const;
