[string]$outputFile = "readme.md"

python code/printInstruction.py > $outputFile

python code/winRateCurve.py >> $outputFile
echo "" >> $outputFile
python code/totalWinRate.py >> $outputFile
echo "" >> $outputFile
python code/totalRoleRate.py >> $outputFile
echo "" >> $outputFile
python code/playerCampRate.py >> $outputFile