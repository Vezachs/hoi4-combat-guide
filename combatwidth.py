# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 12:32:58 2023

"""

# HOW TO USE:
# 1: Copy-paste this code into any compiler such as 
# https://www.codabrainy.com/en/python-compiler/
# 2: Change the number of provinces to whatever you like.
# 3: Run the code.

import numpy as np
import math as math
import matplotlib.pyplot as plt

#Enter the number of provinces for each type you want to simulate, e.g. 500
#Forests, 250 Plains.

Desert = 1
Forest = 1
Hills = 1
Jungle = 1
Marsh = 1
Mountain = 1
Plains = 1
Urban = 1

#Next, enter the weights determining how often you attack from 1,2,3 or 4
#sides. Example: 1,2,1,0.

Attack1province = 1
Attack2province = 2
Attack3province = 1
Attack4province = 0

#Start of the code.

def combatStrength(Terrain_BW,Division_width,ProvinceAttack):
    OverstackMaxDiv = 8 + 4*(ProvinceAttack-1)
    BW = Terrain_BW
    DW = Division_width
    TW = math.ceil(BW / DW) * DW
    CW_penalty = max(1.5 * (TW - BW) / BW, 0)
    if CW_penalty > 0.33:
        TW = math.floor(BW / DW) * DW
        CW_penalty = max(1.5 * (TW - BW) / BW, 0)

    CW_penalty_modifier = 1 - CW_penalty
    Stacking_penalty_modifier = 1 - 0.02* max((TW/DW)-OverstackMaxDiv,0)
    Total_Attack = TW * CW_penalty_modifier*Stacking_penalty_modifier
    AttackValue = Total_Attack / BW
    return AttackValue

#This data is used for making the plots.
TotTerrain = Desert+Forest+Hills+Jungle+Marsh+Mountain+Plains+Urban
DesertRatio = 100* Desert/TotTerrain #Percentage of terrain that is Desert.
ForestRatio = 100* Forest/TotTerrain
HillsRatio = 100* Hills/TotTerrain
JungleRatio = 100* Jungle/TotTerrain
MarshRatio = 100* Marsh/TotTerrain
MountainRatio = 100* Mountain/TotTerrain
PlainsRatio = 100* Plains/TotTerrain
UrbanRatio = 100* Urban/TotTerrain


AttackVec = np.array([Attack1province,Attack2province,Attack3province,Attack4province])

#Here, we use the fact that attacking from 2 sides happens more often than from 1 side.
DesertVec = Desert*AttackVec
ForestVec = Forest*AttackVec
HillsVec = Hills*AttackVec
JungleVec = Jungle*AttackVec
MarshVec = Marsh*AttackVec
MountainVec = Mountain*AttackVec
PlainsVec = Plains*AttackVec
UrbanVec = Urban*AttackVec

TerrainVec = np.concatenate((DesertVec,ForestVec,HillsVec,JungleVec,MarshVec,MountainVec,PlainsVec,UrbanVec), axis=0)
TotalProvinces = np.sum(TerrainVec)
TerrainNormalized = TerrainVec/TotalProvinces

#The base and reinforce combat widths.

BWForest = np.array([60 + 30 * i for i in range(4)])
BWHills = np.array([70 + 35 * i for i in range(4)])
BWJungle = np.array([60 + 30 * i for i in range(4)])
BWMarsh = np.array([50 + 25 * i for i in range(4)])
BWMountain = np.array([50 + 25 * i for i in range(4)])
BWPlains = np.array([70 + 35 * i for i in range(4)])
BWDesert = np.array([70 + 35 * i for i in range(4)])
BWUrban = np.array([80 + 40 * i for i in range(4)])

max_cw = 50


BattleWidths = np.concatenate(([BWDesert,BWForest,BWHills,BWJungle,BWMarsh,BWMountain,BWPlains,BWUrban]), axis=0)
Attacksides = np.tile([1,2,3,4],8) #Array that shows from how many sides one attacks.
AttackTerrain = np.zeros((BattleWidths.size,max_cw))
Division_size = np.arange(1,max_cw)

for k in range(0,BattleWidths.size,1):
    Terrain_BW = BattleWidths[k]
    for l in range(0,Division_size.size,1):
        Division_width = Division_size[l]
        ProvinceAttack = Attacksides[k]
        AttackTerrain[k,l] = combatStrength(Terrain_BW,Division_width,ProvinceAttack)

#WeightedAverages = np.matmul(AttackTerrain,TerrainNormalized)


WeightedAverage = np.zeros((BattleWidths.size,max_cw))
for k in range(0,len(TerrainNormalized),1):
    WeightedAverage[k,:] = AttackTerrain[k,:]*TerrainNormalized[k]
FinalAttack = np.sum(WeightedAverage, axis =0)

##############################################

np.random.seed(19680801)

fig, ax = plt.subplots()
x = np.arange(max_cw-1) + 1
y = np.delete(FinalAttack,max_cw-1)

textstr = '\n'.join((
'Desert: '+str(round(DesertRatio))+'%',
'Forest: '+str(round(ForestRatio))+'%',
'Hills: '+str(round(HillsRatio))+'%',
'Jungle: '+str(round(JungleRatio))+'%',
'Marsh: '+str(round(MarshRatio))+'%',
'Mountain: '+str(round(MountainRatio))+'%',
'Plains: '+str(round(PlainsRatio))+'%',
'Urban: '+str(round(UrbanRatio))+'%' ))

# Create the plot
plt.figure(dpi=300)  # Set the DPI to 300 (adjust the value as needed)

# Plot the data
plt.plot(x, y)

# Set major and minor ticks for y-axis
plt.yticks(np.arange(0.5, 1.06, 0.1))  # Major ticks every 0.1 from 0.5 to 1.0
plt.gca().yaxis.set_minor_locator(plt.MultipleLocator(0.01))  # Minor ticks every 0.01

# Set major and minor ticks for x-axis
plt.xticks(np.arange(0, max_cw + 1, 5))  # Major ticks every 5 from 0 to max_cw
plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(1))  # Minor ticks every 1

# Add labels and title
plt.title('Combat Width simulator by /u/Vezachs')
plt.xlabel('Division Width')
plt.ylabel('Combat Strength')
plt.xlim(0, max_cw)
plt.ylim(0.8, 1.05)

# Show the grid and minor ticks
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.minorticks_on()


plt.text(0.95 * max_cw, 1.04, textstr, fontsize=10, ha='right', va='top',
             bbox=dict(boxstyle='round', facecolor='white', edgecolor='black', alpha=0.8))


plt.show()
