mkdir -p ./data

mkdir -p ./data/invivo
curl -L "https://dataportal.brainminds.jp/download/4822?wpdmdl=4822" -o ./data/invivo/i_Individual_List.zip
curl -L "https://dataportal.brainminds.jp/download/4846?wpdmdl=4846" -o ./data/invivo/i_DiffusionSC.zip
curl -L "https://dataportal.brainminds.jp/download/7994?wpdmdl=7994" -o ./data/invivo/i_Variables_gm.zip
find ./data/invivo -name \*.zip -exec unzip {} -d ./data/invivo/ \; -exec rm {} \;

mkdir -p ./data/exvivo
curl -L "https://dataportal.brainminds.jp/download/4856?wpdmdl=4856" -o ./data/exvivo/e_Individual_List.zip
curl -L "https://dataportal.brainminds.jp/download/4871?wpdmdl=4871" -o ./data/exvivo/e_DiffusionSC.zip
curl -L "https://dataportal.brainminds.jp/download/7995?wpdmdl=7995" -o ./data/exvivo/e_Variables_gm.zip
find ./data/exvivo -name \*.zip -exec unzip {} -d ./data/exvivo/ \; -exec rm {} \;