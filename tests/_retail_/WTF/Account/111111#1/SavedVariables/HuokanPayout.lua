
HuokanPayoutDB = {
	["profileKeys"] = {
		["Name - Realm"] = "Default",
	},
	["profiles"] = {
		["Default"] = {
			["history"] = {
				{
					["input"] = "Player1,1\nPlayer2,2\nPlayer3,3\nPlayer4,4\n",
					["timestamp"] = 0,
					["output"] = "Player4,4",
				}, -- [1]
				{
					["input"] = "Player1,1\nPlayer5,5",
					["timestamp"] = 1,
					["output"] = "",
				}, -- [2]
			},
			["defaultSubject"] = "Payout",
		}, -- [1]
		["Second Profile"] = {
			["history"] = {
				{
					["input"] = "Player1,1\nPlayer6,6",
					["timestamp"] = 2,
					["output"] = "",
				}, -- [1]
			},
		}, -- [2]
	},
}
