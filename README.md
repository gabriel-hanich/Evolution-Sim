# Evolution-Sim
Simulating Natural selection through a population of predators and prey

Note - The frequency distribution between the mean and the variation is given by a Gaussian distribution

# Meaning of Setup Parameters 
> Note: Where a `float` is given, it means any decimal numer, `decimal` means any number between 0 and 1
## Sim
- `length` - **int** - The number of 'turns' the sim has
- `breedTurns` - **int** - After how many turns the animals breed 

## Value Change
- `doChange` - **boolean** Whether or not to change a value after n turns
- `changeTurns` - **int** - After how many turns does the value change
- `keyCategory` - **string** - The category of the key of the value to be changed (`food`, `prey`, etc)
- `key` - **string** - The specific key of the value to be changed
- `changeAmount` - **any** - Number added to the value every change turn

## Board
- `boardSizeX` - **int** - The width of the board the animals inhabit
- `boardSizeY` - **int** - The height of the board
- `fullThreshold` - **decimal** - The percentage of the board that needs to have be occupied before the sim auto ends

## Food
- `foodCount` - **int** - The number of food sources that spawn
- `meanEnergy` - **decimal** - The mean amount of energy provided by a food sources
- `energyVariation` - **decimal** - The variation of amount of energy provided
- `spawnThreshold` - **decimal** The number multiplied by the total population to get when the food sources need replenishing

## Prey
Both health and energy are values between 0 and 1, with 1 being full and 0 being empty (duh)
- `preyCount` - **int** - The number of prey that spawn at the start
- `initEnergy` - **decimal** - The amount of energy prey will spawn with
- `meanSpeed` - **float** - The mean of the speed value a prey will have
- `speedVariation` - **float** How much the speed value will be varied
- `dayCost` - **float** - How strongly prey is penalized at the start of each day
- `meanSensingRange` - **float** - The mean range an animal can sense (see)
- `sensingRangeVariation` - **float** - The variation of the sensing range
- `breedThreshold` - **decimal** - The mininimum amount of energy for a prey to breed at the end of a turn

## Predators
- `predatorCount` - **int** - The number of predators that spawn at the start
- `initEnergy` - **decimal** - The amount of energy prey will spawn with
- `meanSpeed` - **float** - The mean of the speed value a predator will have at the start
- `speedVariation` - **float** - How much the speed value will be varied
- `dayCost` - **float** - How strongly prey is penalized at the start of each day
- `meanSensingRange` - **float** - The mean range an animal can sense (see)
- `sensingRangeVariation` - **float** - The variation of the sensing range
- `breedThreshold` - **decimal** - The mininimum amount of energy for a prey to breed at the end of a turn

# Formula for traits
## Prey
- Efficiency = log(speed + 1) / 20
- Energy Cost from movement = distance * (3 - Efficiency)

# Outputted .csv file format
| Column Letter | Column A | Column B | Column C | Column D | Column E |
| --- | --- | --- | --- | --- | --- |
| Description | Turn Number | Total Prey Population | Average Speed | Average Sensing Range | Number of new prey born THAT turn |