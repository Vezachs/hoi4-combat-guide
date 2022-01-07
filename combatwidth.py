import numpy as np
import math as math
import matplotlib.pyplot as plt

#Enter the number of provinces for each type you want to simulate, e.g. 500
#Forests, 250 Plains.

Desert = 1
Forest = 0
Hills = 0
Jungle = 0
Marsh = 0
Mountain = 0
Plains = 0
Urban = 0

#Next, enter the weights determining how often you attack from 1,2,3 or 4
#sides. Example: 1,2,1,0.

Attack1province = 1
Attack2province = 0
Attack3province = 0
Attack4province = 0

#Start of the code.

def combatStrength(Terrain_BW,Division_width):
    BW = Terrain_BW
    DW = Division_width
    TW = math.ceil(BW / DW) * DW
    CW_penalty = max(1.5 * (TW - BW) / BW, 0)
    if CW_penalty > 0.33:
        TW = math.floor(BW / DW) * DW
        CW_penalty = max(1.5 * (TW - BW) / BW, 0)

    CW_penalty_modifier = 1 - CW_penalty
    Total_Attack = TW * CW_penalty_modifier
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

max_divisions = 75 #The Maximum Division size is 5x5x3=75.
#Combat widths for all terrain types.
BWDesert = np.array([90,90+45,90+2*45,90+3*45])
BWForest = np.array([84,84+42,84+2*42,84+3*42])
BWHills = np.array([80,80+40,80+2*40,80+3*40])
BWJungle = np.array([84,84+42,84+2*42,84+3*42])
BWMarsh = np.array([78,78+26,78+2*26,78+3*26])
BWMountain = np.array([75,75+25,75+2*25,75+3*25])
BWPlains = np.array([90,90+45,90+2*45,90+3*45])
BWUrban = np.array([96,96+32,96+2*32,96+3*32])

BattleWidths = np.concatenate(([BWDesert,BWForest,BWHills,BWJungle,BWMarsh,BWMountain,BWPlains,BWUrban]), axis=0)
AttackTerrain = np.zeros((BattleWidths.size,max_divisions))
Division_size = np.arange(1,max_divisions)

for k in range(0,BattleWidths.size,1):
    Terrain_BW = BattleWidths[k]
    for l in range(0,Division_size.size,1):
        Division_width = Division_size[l]
        AttackTerrain[k,l] = combatStrength(Terrain_BW,Division_width)

#WeightedAverages = np.matmul(AttackTerrain,TerrainNormalized)

WeightedAverage = np.zeros((BattleWidths.size,max_divisions))
for k in range(0,len(TerrainNormalized),1):
    WeightedAverage[k,:] = AttackTerrain[k,:]*TerrainNormalized[k]
FinalAttack = np.sum(WeightedAverage, axis =0)

##############################################

np.random.seed(19680801)

fig, ax = plt.subplots()
x = np.arange(max_divisions-1) + 1
y = np.delete(FinalAttack,max_divisions-1)

textstr = '\n'.join((
'Desert: '+str(DesertRatio)+'%',
'Forest: '+str(ForestRatio)+'%',
'Hills: '+str(HillsRatio)+'%',
'Jungle: '+str(JungleRatio)+'%',
'Marsh: '+str(MarshRatio)+'%',
'Mountain: '+str(MountainRatio)+'%',
'Plains: '+str(PlainsRatio)+'%',
'Urban: '+str(UrbanRatio)+'%' ))

plt.plot(x,y)
plt.title('Combat Width simulator by /u/Vezachs')
plt.xlabel('Division Width')
plt.ylabel('Combat Strength')
plt.xlim(0, max_divisions)
plt.ylim(0.5, 1.05)

major_ticks_x=np.arange(0,75,5)
minor_ticks_x=np.arange(0,75,1)
major_ticks_y=np.arange(0.5,1.1,0.1)
minor_ticks_y=np.arange(0.5,1.1,0.02)

ax.set_xticks(major_ticks_x)
ax.set_yticks(major_ticks_y)
ax.set_xticks(minor_ticks_x,minor=True)
ax.set_yticks(minor_ticks_y,minor=True)
ax.grid(which="major",alpha=0.6)
ax.grid(which="minor",alpha=0.3)

# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='white', alpha=1)

# place a text box in upper left in axes coords
ax.text(0.05, 0.4, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

plt.show()
