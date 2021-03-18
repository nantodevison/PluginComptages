# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CeremaSoComptagesDialog
                                 A QGIS plugin
 Gestion de trafics Cerema SO
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-10-17
        git sha              : $Format:%H$
        copyright            : (C) 2020 by martin Schoreisz
        email                : martin.schoreisz@cerema.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets,QtGui
from qgis.PyQt.QtWidgets import QGroupBox,QCheckBox
from PyQt5.QtCore import pyqtSlot
import ceremaso_comptages.Donnees_sources as di

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS_base, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ceremaso_comptages_dialog_base.ui'))

FORM_CLASS_traiterPt, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ceremaso_comptages_dialog_traiter_pt_comptage.ui'))

FORM_CLASS_VisuExport, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ceremaso_comptages_dialog_visu-export.ui'))

FORM_CLASS_DonneesType, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ceremaso_comptages_dialog_donnees_type.ui'))

class CeremaSoComptagesDialog(QtWidgets.QDialog, FORM_CLASS_base):
    def __init__(self, parent=None):
        """Constructor."""
        super(CeremaSoComptagesDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        #signal/slots
        self.pushButtonTraiterPointComptage.clicked.connect(self.ouvrirDonneesType)
        
            
    def ouvrirDonneesType(self):
        """
        ouvrir la fenetre de la classe CeremaSoComptagesTraiterPtDialog
        """
        self.fenetreDonneesType=CeremaSoComptagesDonneesType()
        self.fenetreDonneesType.show()
        result = self.fenetreDonneesType.exec_()
        # See if OK was pressed
        if result:
            pass
        
        
            
class CeremaSoComptagesDonneesType(QtWidgets.QDialog, FORM_CLASS_DonneesType):
    def __init__(self, parent=None):
        """Constructor."""
        super(CeremaSoComptagesDonneesType, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.ouvrirTraiterPtDialog)
    
    def ouvrirTraiterPtDialog(self):
        """
        ouvrir la fenetre de la classe CeremaSoComptagesTraiterPtDialog
        """
        donneesType='Fim' if self.radioButtonFim.isChecked() else 'Indiv'
        print(f'donneesType = {donneesType}')
        vitesse=self.checkBoxVitesse.isChecked()
        print(f'Prise en compte vitesse : {vitesse}')
        self.fenetreTraiterPt=CeremaSoComptagesTraiterPtDialog(donneesType, vitesse)
        self.fenetreTraiterPt.show()

       
    
        
class CeremaSoComptagesTraiterPtDialog(QtWidgets.QDialog, FORM_CLASS_traiterPt):
    def __init__(self,donneesType,vitesse, parent=None):
        """Constructor."""
        self.donneesType=donneesType
        self.vitesse=vitesse
        super(CeremaSoComptagesTraiterPtDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        #signal/slots
        self.radioButtonTraiterCpt1Fichier.toggled.connect(self.basculerQgisFileWidget)
        self.radioButtonTraiterCpt1point.toggled.connect(self.basculerQgisFileWidget)
        self.radioButtonTraiterCptPlusieursPt.toggled.connect(self.basculerQgisFileWidget)
        self.buttonBox.accepted.connect(self.ouvrirVisuExport)
        
    
    @pyqtSlot()
    def basculerQgisFileWidget(self):
        dicoBoutonChoix={'radioButtonTraiterCpt1Fichier':self.mQgsFileWidgetTraiter1sens,
                        'radioButtonTraiterCpt1point':self.mQgsFileWidgetTraiter1Point,
                        'radioButtonTraiterCptPlusieursPt' : self.mQgsFileWidgetTraiterPlusieursPoints}
        for k, v in dicoBoutonChoix.items() :
            if self.sender().objectName()==k : 
                if not v.isEnabled() :
                    v.setEnabled(True)
                else : 
                    v.setEnabled(False)
    
    @pyqtSlot()
    def ouvrirVisuExport(self):
        """
        recuprere le text du widget qui est allume et ouvre la fenetre suivante
        """
        for t,w in {'fichiers':self.mQgsFileWidgetTraiter1sens, '1Point':self.mQgsFileWidgetTraiter1Point,
                    'plusieursPoints':self.mQgsFileWidgetTraiterPlusieursPoints}.items() : 
            if w.isEnabled() : 
                source=w.splitFilePaths(w.filePath())
                typeTraitement=t
                break
                
        self.fenetreVisuExport=CeremaSoComptagesVisuExport(self.donneesType,self.vitesse,typeTraitement,source)
        self.fenetreVisuExport.show()
        self.fenetreVisuExport.activateWindow()
        
class CeremaSoComptagesVisuExport(QtWidgets.QDialog, FORM_CLASS_VisuExport):
    def __init__(self, donneesType,vitesse,typeTraite,source,parent=None):
        """Constructor."""
        super(CeremaSoComptagesVisuExport, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.visuGraph)
        self.groupBoxVisu.toggled.connect(self.basculeGroupBox)
        self.groupBoxExport.toggled.connect(self.basculeGroupBox)
        self.groupBoxSynthese.toggled.connect(self.basculeSyntheseDetail)
        self.groupBoxDetails.toggled.connect(self.basculeSyntheseDetail)
        
        
        
        self.typeTraite=typeTraite
        self.source=source
        self.donneesType=donneesType
        self.vitesse=vitesse
        print(f'type_traite : {self.typeTraite}')
        self.cpt=self.calculDfComptage()
        self.filtrerTypeVehPossible()
        
    def calculDfComptage(self):
        if self.typeTraite=='1Point' : #cas ou on choisit de traiter 1 point de comptage complet
            if self.donneesType=='Indiv' :
                cpt=di.ComptageDonneesIndiv(self.source[0], self.vitesse)
            else :
                cpt=di.ComptageFim(self.source[0])
        
        ### EN COURS POINT D'ARRET###########
        """elif self.typeTraite=='fichiers' : #ca sou on choisit de traiter un fichier 
            if self.donneesType=='Indiv' :
                cpt=
        """
        
        return cpt
    
    def filtrerTypeVehPossible(self):
        """
        selon les donnes de comptage, filtrer les typs de veh dispo ou non
        """
        dicoTypeVeh={'vl':[self.checkBoxVlSynthese,self.checkBoxVlDetails], 'pl':[self.checkBoxPlSynthese,self.checkBoxPlDetails], 
                     '2r':[self.checkBox2rSynthese,self.checkBox2rDetails], 'tv':[self.checkBoxTvSynthese,self.checkBoxTvDetails]}
        for k,v in dicoTypeVeh.items() :
            if k not in self.cpt.dfSemaineMoyenne.type_veh.unique() :
                print(f'{k} pas dan sdico')
                for w in v : 
                    print(k,w)
                    w.setEnabled(False)
        
    
    def trouverTypeVisu(self):
        """
        renvoyer si on veut synthese ou detail
        """
        if self.groupBoxSynthese.isChecked() : 
            return 'synthese'
        else :
            return 'details'
    
    def trouverCheckBoxOn(self):
        if self.groupBoxVisu.isChecked() : 
            listPeriod=[cb.text().lower().replace(' ','') for cb in self.groupBoxVisuPeriode.findChildren(QCheckBox) if cb.isChecked()]
            listSens=[cb.text().lower().replace(' ','') for cb in self.groupBoxVisuSens.findChildren(QCheckBox) if cb.isChecked()]
            listTypeVeh=[cb.text().lower().replace(' ','') for cb in self.groupBoxTypeVeh.findChildren(QCheckBox) if cb.isChecked()]
        if self.groupBoxSynthese.isChecked() : 
            listPeriod=[]
            listSens=[]
            listTypeVeh=[cb.text().lower().replace(' ','') for cb in self.groupBoxSynthese.findChildren(QCheckBox) if cb.isChecked()]
        return listPeriod,listSens,listTypeVeh
    
    @pyqtSlot()
    def basculeSyntheseDetail(self):
        """
        basculer entre synthese et detail, les deux se rejettent
        """
        if self.sender().isChecked() :
            self.filtrerTypeVehPossible()
            if self.sender()==self.groupBoxSynthese:
                self.groupBoxDetails.setEnabled(False)
                self.groupBoxDetails.setChecked(False)
            else : 
                self.groupBoxSynthese.setEnabled(False)
                self.groupBoxSynthese.setChecked(False)
        else : 
            if self.sender()==self.groupBoxSynthese:
                self.groupBoxDetails.setEnabled(True) 
                self.groupBoxDetails.setChecked(True)
                self.filtrerTypeVehPossible()
            else : 
                self.groupBoxSynthese.setEnabled(True)
                self.groupBoxSynthese.setChecked(True)
                self.filtrerTypeVehPossible()
    
    @pyqtSlot()
    def visuGraph(self):
        listPeriod,listSens,listTypeVeh=self.trouverCheckBoxOn()
        print(listPeriod,listSens,listTypeVeh,self.vitesse)
        if self.trouverTypeVisu()=='details' :
            self.cpt.graphsSynthese(listTypeVeh, listPeriod, listSens,self.vitesse)
            for p in listPeriod :
                for s in listSens :
                    print(p, s)
                    self.cpt.dicoHoraire[p][s]['graph'].show()
                    if p=='mja' :
                        self.cpt.dicoJournalier[p][s]['graph'].show()
                        if s=='2sens' : 
                            self.cpt.dicoJournalier[p]['compSens']['graph'].show()
        else :
            figSyntheses, figJournaliere=self.cpt.graphsSynthese(listTypeVeh, vitesse=self.vitesse,synthese=True)
            figSyntheses.show()
            figJournaliere.show()
    
    @pyqtSlot()
    def basculeGroupBox(self):
        if self.sender().isChecked():
            if self.sender().objectName()=='groupBoxVisu' : 
                self.groupBoxExport.setEnabled(False)
            else :
                self.groupBoxVisu.setEnabled(False)
        else :
            if self.sender().objectName()=='groupBoxVisu' : 
                self.groupBoxExport.setEnabled(True)
            else : 
                self.groupBoxVisu.setEnabled(True)
