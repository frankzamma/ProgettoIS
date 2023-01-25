package Logics.machinelearning;


import Model.MeteoInformation;
import Model.Pantaloni;
import Model.ScoreCapoAbbigliamento;

import java.util.List;

public class BottomML {

    private RegressionTreeWrapper treeWrapper;

    public BottomML(String pathDataset){
        //Si crea e si addestra il l'albero di regressione
        treeWrapper = new RegressionTreeWrapper(pathDataset,false, true, "PantaloniML");
    }

    public List<ScoreCapoAbbigliamento> classifyInstances(List<Pantaloni> list, MeteoInformation meteo, boolean getBestThree){
        List<ScoreCapoAbbigliamento> scoreCapoAbbigliamentoList = treeWrapper.classifyInstances(list, meteo);
        if(getBestThree)
            return treeWrapper.getBestThreeClothes(scoreCapoAbbigliamentoList);
        else
            return scoreCapoAbbigliamentoList;
    }
}
