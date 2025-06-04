#show pv_AP1/0.
pv_AP1, nv_AP1.
nv_AP1 :- nv_AP1.
#show nv_AP1/0.
pv_AP1 :- pv_AP1.
#show pv_Akt/0.
pv_Akt, nv_Akt.
nv_Akt :- nv_Tox2.
#show nv_Akt/0.
pv_Akt :- pv_Tox2.
#show pv_B9/0.
pv_B9, nv_B9.
nv_B9 :- nv_B9.
#show nv_B9/0.
pv_B9 :- pv_B9.
#show pv_BCR/0.
pv_BCR, nv_BCR.
nv_BCR :- nv_BCR.
#show nv_BCR/0.
pv_BCR :- pv_BCR.
#show pv_Bach2/0.
pv_Bach2, nv_Bach2.
nv_Bach2 :- nv_PDK1.
nv_Bach2 :- nv_Bcl11b.
#show nv_Bach2/0.
pv_Bach2 :- pv_PDK1, pv_Bcl11b.
#show pv_Bcl11b/0.
pv_Bcl11b, nv_Bcl11b.
nv_Bcl11b :- nv_CD8.
nv_Bcl11b :- nv_Pax5.
nv_Bcl11b :- nv_CD19.
#show nv_Bcl11b/0.
pv_Bcl11b :- pv_CD8, pv_Pax5, pv_CD19.
#show pv_Bcl2/0.
pv_Bcl2, nv_Bcl2.
nv_Bcl2 :- nv_GATA3.
nv_Bcl2 :- nv_STAT6.
#show nv_Bcl2/0.
pv_Bcl2 :- pv_GATA3, pv_STAT6.
#show pv_Bcl6/0.
pv_Bcl6, nv_Bcl6.
nv_Bcl6 :- pv_JAK1, pv_CD4, nv_IL23, nv_EOMES.
#show nv_Bcl6/0.
pv_Bcl6 :- nv_JAK1.
pv_Bcl6 :- nv_CD4.
pv_Bcl6 :- pv_IL23.
pv_Bcl6 :- pv_EOMES.
#show pv_Blimp1/0.
pv_Blimp1, nv_Blimp1.
nv_Blimp1 :- nv_JAK1, pv_PDK1, pv_Bcl2, pv_Bcl11b.
#show nv_Blimp1/0.
pv_Blimp1 :- pv_JAK1.
pv_Blimp1 :- nv_PDK1.
pv_Blimp1 :- nv_Bcl2.
pv_Blimp1 :- nv_Bcl11b.
#show pv_CD122/0.
pv_CD122, nv_CD122.
nv_CD122 :- nv_Flt3L.
nv_CD122 :- nv_E2A.
nv_CD122 :- nv_ERK, nv_SMAD2, pv_BCR.
#show nv_CD122/0.
aux_0_0 :- pv_ERK.
aux_0_0 :- pv_SMAD2.
aux_0_0 :- nv_BCR.
pv_CD122 :- pv_Flt3L, pv_E2A, aux_0_0.
#show pv_CD19/0.
pv_CD19, nv_CD19.
nv_CD19 :- nv_PDK1.
#show nv_CD19/0.
pv_CD19 :- pv_PDK1.
#show pv_CD4/0.
pv_CD4, nv_CD4.
aux_0_1 :- nv_Pax5.
aux_0_1 :- nv_TNFa.
aux_0_1 :- nv_CD8, nv_CD19.
nv_CD4 :- pv_SMAD2, pv_EOMES, aux_0_1.
#show nv_CD4/0.
pv_CD4 :- nv_SMAD2.
pv_CD4 :- nv_EOMES.
aux_0_2 :- pv_CD8.
aux_0_2 :- pv_CD19.
pv_CD4 :- pv_Pax5, pv_TNFa, aux_0_2.
#show pv_CD8/0.
pv_CD8, nv_CD8.
aux_0_3 :- nv_SMAD2.
aux_0_3 :- nv_Pax5.
aux_0_3 :- nv_CD8, nv_CD19.
nv_CD8 :- nv_BCR, pv_TGFb, pv_EOMES, pv_TNFa, aux_0_3.
#show nv_CD8/0.
pv_CD8 :- pv_BCR.
pv_CD8 :- nv_TGFb.
pv_CD8 :- nv_EOMES.
pv_CD8 :- nv_TNFa.
pv_CD8 :- pv_SMAD2, pv_Pax5, aux_0_2.
#show pv_E2A/0.
pv_E2A, nv_E2A.
nv_E2A :- nv_PDK1, pv_IFNb, nv_EOMES, pv_HES1.
#show nv_E2A/0.
pv_E2A :- pv_PDK1.
pv_E2A :- nv_IFNb.
pv_E2A :- pv_EOMES.
pv_E2A :- nv_HES1.
#show pv_E4BP4/0.
pv_E4BP4, nv_E4BP4.
nv_E4BP4 :- nv_Prf1, pv_BCR.
#show nv_E4BP4/0.
pv_E4BP4 :- pv_Prf1.
pv_E4BP4 :- nv_BCR.
#show pv_EOMES/0.
pv_EOMES, nv_EOMES.
aux_0_4 :- nv_IRAK.
aux_0_4 :- nv_TCF1.
aux_0_4 :- nv_Flt3.
nv_EOMES :- nv_SMAD2, aux_0_4.
#show nv_EOMES/0.
pv_EOMES :- pv_SMAD2.
pv_EOMES :- pv_IRAK, pv_TCF1, pv_Flt3.
#show pv_ERK/0.
pv_ERK, nv_ERK.
nv_ERK :- nv_Blimp1.
nv_ERK :- nv_Flt3L.
#show nv_ERK/0.
pv_ERK :- pv_Blimp1, pv_Flt3L.
#show pv_ETS1/0.
pv_ETS1, nv_ETS1.
nv_ETS1 :- nv_NFkB.
nv_ETS1 :- nv_IFNb.
#show nv_ETS1/0.
pv_ETS1 :- pv_NFkB, pv_IFNb.
#show pv_Ebf1/0.
pv_Ebf1, nv_Ebf1.
nv_Ebf1 :- nv_Runx3, pv_SMAD2.
#show nv_Ebf1/0.
pv_Ebf1 :- pv_Runx3.
pv_Ebf1 :- nv_SMAD2.
#show pv_FR4/0.
pv_FR4, nv_FR4.
nv_FR4 :- nv_Bach2, nv_FR4.
#show nv_FR4/0.
pv_FR4 :- pv_Bach2.
pv_FR4 :- pv_FR4.
#show pv_Flt3/0.
pv_Flt3, nv_Flt3.
aux_0_5 :- nv_ICOS.
aux_0_5 :- nv_Foxo1.
nv_Flt3 :- pv_PDK1, aux_0_5.
#show nv_Flt3/0.
pv_Flt3 :- nv_PDK1.
pv_Flt3 :- pv_ICOS, pv_Foxo1.
#show pv_Flt3L/0.
pv_Flt3L, nv_Flt3L.
nv_Flt3L :- nv_Flt3L.
#show nv_Flt3L/0.
pv_Flt3L :- pv_Flt3L.
#show pv_Foxo1/0.
pv_Foxo1, nv_Foxo1.
nv_Foxo1 :- pv_NFkB, pv_Prf1, nv_EOMES, nv_E4BP4.
#show nv_Foxo1/0.
pv_Foxo1 :- nv_NFkB.
pv_Foxo1 :- nv_Prf1.
pv_Foxo1 :- pv_EOMES.
pv_Foxo1 :- pv_E4BP4.
#show pv_Foxp3/0.
pv_Foxp3, nv_Foxp3.
aux_0_6 :- nv_SOCS1.
aux_0_6 :- nv_SMAD3.
aux_0_6 :- nv_FR4.
nv_Foxp3 :- pv_STAT4, pv_TCF1, pv_Runx1, pv_Gfi1, nv_TNFa, aux_0_6.
#show nv_Foxp3/0.
pv_Foxp3 :- nv_STAT4.
pv_Foxp3 :- nv_TCF1.
pv_Foxp3 :- nv_Runx1.
pv_Foxp3 :- nv_Gfi1.
pv_Foxp3 :- pv_TNFa.
pv_Foxp3 :- pv_SOCS1, pv_SMAD3, pv_FR4.
#show pv_GATA3/0.
pv_GATA3, nv_GATA3.
aux_0_7 :- nv_TCR.
aux_0_7 :- nv_Tbet.
aux_0_7 :- nv_Gfi1.
nv_GATA3 :- pv_Runx3, pv_TCF1, pv_FR4, pv_Runx1, nv_TNFa, pv_HES1, aux_0_7.
#show nv_GATA3/0.
pv_GATA3 :- nv_Runx3.
pv_GATA3 :- nv_TCF1.
pv_GATA3 :- nv_FR4.
pv_GATA3 :- nv_Runx1.
pv_GATA3 :- pv_TNFa.
pv_GATA3 :- nv_HES1.
pv_GATA3 :- pv_TCR, pv_Tbet, pv_Gfi1.
#show pv_Gfi1/0.
pv_Gfi1, nv_Gfi1.
nv_Gfi1 :- nv_IL2.
#show nv_Gfi1/0.
pv_Gfi1 :- pv_IL2.
#show pv_Gzmb/0.
pv_Gzmb, nv_Gzmb.
nv_Gzmb :- nv_ERK.
#show nv_Gzmb/0.
pv_Gzmb :- pv_ERK.
#show pv_HEB/0.
pv_HEB, nv_HEB.
nv_HEB :- nv_Pax5, pv_IFNb.
#show nv_HEB/0.
pv_HEB :- pv_Pax5.
pv_HEB :- nv_IFNb.
#show pv_HES1/0.
pv_HES1, nv_HES1.
nv_HES1 :- pv_RORgt, nv_Pax5.
#show nv_HES1/0.
pv_HES1 :- nv_RORgt.
pv_HES1 :- pv_Pax5.
#show pv_Helios/0.
pv_Helios, nv_Helios.
nv_Helios :- nv_NFAT.
#show nv_Helios/0.
pv_Helios :- pv_NFAT.
#show pv_ICOS/0.
pv_ICOS, nv_ICOS.
nv_ICOS :- nv_B9.
#show nv_ICOS/0.
pv_ICOS :- pv_B9.
#show pv_IFNb/0.
pv_IFNb, nv_IFNb.
nv_IFNb :- nv_IFNb.
#show nv_IFNb/0.
pv_IFNb :- pv_IFNb.
#show pv_IFNg/0.
pv_IFNg, nv_IFNg.
nv_IFNg :- nv_SMAD2, nv_TCF1.
aux_0_8 :- nv_STAT5.
aux_0_8 :- nv_Irf4.
aux_0_8 :- nv_TCF1.
nv_IFNg :- pv_STAT4, aux_0_8.
#show nv_IFNg/0.
aux_0_9 :- pv_SMAD2.
aux_0_9 :- pv_TCF1.
aux_0_10 :- nv_STAT4.
aux_0_10 :- pv_STAT5, pv_Irf4, pv_TCF1.
pv_IFNg :- aux_0_9, aux_0_10.
#show pv_IL10/0.
pv_IL10, nv_IL10.
nv_IL10 :- nv_Gfi1.
#show nv_IL10/0.
pv_IL10 :- pv_Gfi1.
#show pv_IL12/0.
pv_IL12, nv_IL12.
nv_IL12 :- nv_IL12.
#show nv_IL12/0.
pv_IL12 :- pv_IL12.
#show pv_IL12R/0.
pv_IL12R, nv_IL12R.
nv_IL12R :- pv_Tbet, nv_IL12R.
#show nv_IL12R/0.
pv_IL12R :- nv_Tbet.
pv_IL12R :- pv_IL12R.
#show pv_IL15/0.
pv_IL15, nv_IL15.
nv_IL15 :- nv_IL15.
#show nv_IL15/0.
pv_IL15 :- pv_IL15.
#show pv_IL17/0.
pv_IL17, nv_IL17.
nv_IL17 :- nv_Runx1.
nv_IL17 :- nv_Notch1, nv_B9.
#show nv_IL17/0.
aux_0_11 :- pv_Notch1.
aux_0_11 :- pv_B9.
pv_IL17 :- pv_Runx1, aux_0_11.
#show pv_IL18R/0.
pv_IL18R, nv_IL18R.
nv_IL18R :- pv_Tbet, nv_IL18R.
#show nv_IL18R/0.
pv_IL18R :- nv_Tbet.
pv_IL18R :- pv_IL18R.
#show pv_IL2/0.
pv_IL2, nv_IL2.
nv_IL2 :- nv_IL2.
#show nv_IL2/0.
pv_IL2 :- pv_IL2.
#show pv_IL21/0.
pv_IL21, nv_IL21.
nv_IL21 :- nv_IL21.
#show nv_IL21/0.
pv_IL21 :- pv_IL21.
#show pv_IL23/0.
pv_IL23, nv_IL23.
nv_IL23 :- nv_IL23.
#show nv_IL23/0.
pv_IL23 :- pv_IL23.
#show pv_IL27/0.
pv_IL27, nv_IL27.
nv_IL27 :- nv_IL27.
#show nv_IL27/0.
pv_IL27 :- pv_IL27.
#show pv_IL4/0.
pv_IL4, nv_IL4.
nv_IL4 :- pv_STAT3, nv_Gfi1.
#show nv_IL4/0.
pv_IL4 :- nv_STAT3.
pv_IL4 :- pv_Gfi1.
#show pv_IL4R/0.
pv_IL4R, nv_IL4R.
nv_IL4R :- pv_STAT1, nv_IL4R.
#show nv_IL4R/0.
pv_IL4R :- nv_STAT1.
pv_IL4R :- pv_IL4R.
#show pv_IL6/0.
pv_IL6, nv_IL6.
nv_IL6 :- nv_Runx1.
#show nv_IL6/0.
pv_IL6 :- pv_Runx1.
#show pv_IL7/0.
pv_IL7, nv_IL7.
nv_IL7 :- nv_IL7.
#show nv_IL7/0.
pv_IL7 :- pv_IL7.
#show pv_IL7R/0.
pv_IL7R, nv_IL7R.
nv_IL7R :- nv_IL7R, pv_TGFb.
#show nv_IL7R/0.
pv_IL7R :- pv_IL7R.
pv_IL7R :- nv_TGFb.
#show pv_IRAK/0.
pv_IRAK, nv_IRAK.
nv_IRAK :- nv_IL21.
#show nv_IRAK/0.
pv_IRAK :- pv_IL21.
#show pv_Id2/0.
pv_Id2, nv_Id2.
aux_0_12 :- nv_Flt3.
aux_0_12 :- nv_E2A.
nv_Id2 :- pv_BCR, pv_EOMES, pv_TNFa, aux_0_12.
#show nv_Id2/0.
pv_Id2 :- nv_BCR.
pv_Id2 :- nv_EOMES.
pv_Id2 :- nv_TNFa.
pv_Id2 :- pv_Flt3, pv_E2A.
#show pv_Ikaros/0.
pv_Ikaros, nv_Ikaros.
nv_Ikaros :- nv_RORgt.
#show nv_Ikaros/0.
pv_Ikaros :- pv_RORgt.
#show pv_Irf4/0.
pv_Irf4, nv_Irf4.
aux_0_13 :- nv_NFAT.
aux_0_13 :- nv_CD4.
nv_Irf4 :- nv_EOMES, pv_Flt3L, aux_0_13.
#show nv_Irf4/0.
pv_Irf4 :- pv_EOMES.
pv_Irf4 :- nv_Flt3L.
pv_Irf4 :- pv_NFAT, pv_CD4.
#show pv_JAK1/0.
pv_JAK1, nv_JAK1.
nv_JAK1 :- nv_Ikaros.
#show nv_JAK1/0.
pv_JAK1 :- pv_Ikaros.
#show pv_JAK3/0.
pv_JAK3, nv_JAK3.
aux_0_14 :- nv_IL10.
aux_0_14 :- nv_IL7.
nv_JAK3 :- pv_Pax5, aux_0_14.
#show nv_JAK3/0.
pv_JAK3 :- nv_Pax5.
pv_JAK3 :- pv_IL10, pv_IL7.
#show pv_MAPK/0.
pv_MAPK, nv_MAPK.
nv_MAPK :- nv_IL17.
#show nv_MAPK/0.
pv_MAPK :- pv_IL17.
#show pv_NFAT/0.
pv_NFAT, nv_NFAT.
nv_NFAT :- nv_TGFb.
#show nv_NFAT/0.
pv_NFAT :- pv_TGFb.
#show pv_NFkB/0.
pv_NFkB, nv_NFkB.
nv_NFkB :- nv_Blimp1.
#show nv_NFkB/0.
pv_NFkB :- pv_Blimp1.
#show pv_Notch1/0.
pv_Notch1, nv_Notch1.
nv_Notch1 :- nv_Notch1.
#show nv_Notch1/0.
pv_Notch1 :- pv_Notch1.
#show pv_PDK1/0.
pv_PDK1, nv_PDK1.
nv_PDK1 :- nv_IL17.
#show nv_PDK1/0.
pv_PDK1 :- pv_IL17.
#show pv_PU1/0.
pv_PU1, nv_PU1.
nv_PU1 :- pv_IL2, pv_Gzmb.
#show nv_PU1/0.
pv_PU1 :- nv_IL2.
pv_PU1 :- nv_Gzmb.
#show pv_Pax5/0.
pv_Pax5, nv_Pax5.
nv_Pax5 :- pv_JAK1, pv_CD4, nv_EOMES, pv_Flt3L, pv_TNFa.
nv_Pax5 :- pv_JAK1, pv_CD4, nv_STAT6, nv_EOMES, pv_TNFa.
#show nv_Pax5/0.
aux_0_15 :- nv_JAK1.
aux_0_15 :- nv_CD4.
aux_0_15 :- pv_EOMES.
aux_0_15 :- nv_Flt3L.
aux_0_15 :- nv_TNFa.
aux_0_16 :- nv_JAK1.
aux_0_16 :- nv_CD4.
aux_0_16 :- pv_STAT6.
aux_0_16 :- pv_EOMES.
aux_0_16 :- nv_TNFa.
pv_Pax5 :- aux_0_15, aux_0_16.
#show pv_Prf1/0.
pv_Prf1, nv_Prf1.
nv_Prf1 :- nv_ERK, nv_TCF1.
#show nv_Prf1/0.
pv_Prf1 :- pv_ERK.
pv_Prf1 :- pv_TCF1.
#show pv_RORgt/0.
pv_RORgt, nv_RORgt.
aux_0_17 :- nv_STAT4.
aux_0_17 :- nv_Runx1.
nv_RORgt :- pv_TCF1, pv_FR4, pv_Gfi1, nv_TNFa, aux_0_17.
#show nv_RORgt/0.
pv_RORgt :- nv_TCF1.
pv_RORgt :- nv_FR4.
pv_RORgt :- nv_Gfi1.
pv_RORgt :- pv_TNFa.
pv_RORgt :- pv_STAT4, pv_Runx1.
#show pv_Runx1/0.
pv_Runx1, nv_Runx1.
nv_Runx1 :- nv_Runx3, pv_SMAD2, pv_Pax5, pv_TGFb, pv_TNFa.
#show nv_Runx1/0.
pv_Runx1 :- pv_Runx3.
pv_Runx1 :- nv_SMAD2.
pv_Runx1 :- nv_Pax5.
pv_Runx1 :- nv_TGFb.
pv_Runx1 :- nv_TNFa.
#show pv_Runx3/0.
pv_Runx3, nv_Runx3.
nv_Runx3 :- nv_E2A.
nv_Runx3 :- pv_CD8, pv_STAT6, nv_CD19, pv_TNFa.
nv_Runx3 :- nv_STAT6, nv_CD19.
#show nv_Runx3/0.
aux_0_18 :- pv_CD8, pv_STAT6, pv_CD19.
aux_0_18 :- pv_CD8, pv_STAT6, nv_CD19, nv_TNFa.
aux_0_18 :- pv_CD8, nv_STAT6, pv_CD19.
aux_0_18 :- nv_CD8, pv_STAT6.
aux_0_18 :- nv_CD8, nv_STAT6, pv_CD19.
pv_Runx3 :- pv_E2A, aux_0_18.
#show pv_SMAD2/0.
pv_SMAD2, nv_SMAD2.
nv_SMAD2 :- nv_ThPOK.
#show nv_SMAD2/0.
pv_SMAD2 :- pv_ThPOK.
#show pv_SMAD3/0.
pv_SMAD3, nv_SMAD3.
nv_SMAD3 :- pv_AP1, nv_ThPOK.
#show nv_SMAD3/0.
pv_SMAD3 :- nv_AP1.
pv_SMAD3 :- pv_ThPOK.
#show pv_SOCS1/0.
pv_SOCS1, nv_SOCS1.
nv_SOCS1 :- nv_STAT3.
nv_SOCS1 :- nv_TCF1.
#show nv_SOCS1/0.
pv_SOCS1 :- pv_STAT3, pv_TCF1.
#show pv_STAT1/0.
pv_STAT1, nv_STAT1.
nv_STAT1 :- nv_IFNg.
nv_STAT1 :- nv_IRAK.
nv_STAT1 :- nv_JAK3.
#show nv_STAT1/0.
pv_STAT1 :- pv_IFNg, pv_IRAK, pv_JAK3.
#show pv_STAT3/0.
pv_STAT3, nv_STAT3.
nv_STAT3 :- nv_MAPK.
nv_STAT3 :- nv_IL12.
nv_STAT3 :- nv_IL23.
nv_STAT3 :- nv_IL27.
#show nv_STAT3/0.
pv_STAT3 :- pv_MAPK, pv_IL12, pv_IL23, pv_IL27.
#show pv_STAT4/0.
pv_STAT4, nv_STAT4.
nv_STAT4 :- nv_IL15, pv_Gfi1.
#show nv_STAT4/0.
pv_STAT4 :- pv_IL15.
pv_STAT4 :- nv_Gfi1.
#show pv_STAT5/0.
pv_STAT5, nv_STAT5.
aux_0_19 :- nv_MAPK.
aux_0_19 :- nv_IL4.
nv_STAT5 :- pv_STAT1, aux_0_19.
#show nv_STAT5/0.
pv_STAT5 :- nv_STAT1.
pv_STAT5 :- pv_MAPK, pv_IL4.
#show pv_STAT6/0.
pv_STAT6, nv_STAT6.
nv_STAT6 :- nv_IL6.
#show nv_STAT6/0.
pv_STAT6 :- pv_IL6.
#show pv_TCF1/0.
pv_TCF1, nv_TCF1.
nv_TCF1 :- nv_Pax5.
#show nv_TCF1/0.
pv_TCF1 :- pv_Pax5.
#show pv_TCR/0.
pv_TCR, nv_TCR.
nv_TCR :- nv_TCR.
#show nv_TCR/0.
pv_TCR :- pv_TCR.
#show pv_TGFb/0.
pv_TGFb, nv_TGFb.
nv_TGFb :- nv_FR4.
#show nv_TGFb/0.
pv_TGFb :- pv_FR4.
#show pv_TNFa/0.
pv_TNFa, nv_TNFa.
nv_TNFa :- nv_Runx1.
#show nv_TNFa/0.
pv_TNFa :- pv_Runx1.
#show pv_Tbet/0.
pv_Tbet, nv_Tbet.
aux_0_20 :- nv_STAT3.
aux_0_20 :- nv_TCF1.
nv_Tbet :- pv_FR4, pv_Runx1, pv_Gfi1, aux_0_20.
#show nv_Tbet/0.
pv_Tbet :- nv_FR4.
pv_Tbet :- nv_Runx1.
pv_Tbet :- nv_Gfi1.
pv_Tbet :- pv_STAT3, pv_TCF1.
#show pv_ThPOK/0.
pv_ThPOK, nv_ThPOK.
aux_0_21 :- nv_TGFb.
aux_0_21 :- nv_TCF1.
aux_0_21 :- nv_FR4.
aux_0_21 :- nv_Runx1.
aux_0_21 :- nv_Gfi1.
aux_0_21 :- nv_TNFa.
nv_ThPOK :- pv_SMAD2, aux_0_21.
#show nv_ThPOK/0.
pv_ThPOK :- nv_SMAD2.
pv_ThPOK :- pv_TGFb, pv_TCF1, pv_FR4, pv_Runx1, pv_Gfi1, pv_TNFa.
#show pv_Tox2/0.
pv_Tox2, nv_Tox2.
nv_Tox2 :- nv_E2A.
#show nv_Tox2/0.
pv_Tox2 :- pv_E2A.
#show pv_XBP1/0.
pv_XBP1, nv_XBP1.
nv_XBP1 :- nv_CD4.
#show nv_XBP1/0.
pv_XBP1 :- pv_CD4.
#show pv_l_notch1/0.
pv_l_notch1, nv_l_notch1.
nv_l_notch1 :- nv_Ebf1.
#show nv_l_notch1/0.
pv_l_notch1 :- pv_Ebf1.
