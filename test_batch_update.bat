@echo off
echo Test de mise a jour par lots des metadonnees SEO
echo =============================================
echo.

REM Verification de l'existence du fichier Python
if not exist test_batch_update.py (
    echo ERREUR: Le fichier test_batch_update.py n'existe pas.
    echo Assurez-vous d'etre dans le bon repertoire.
    goto end
)

REM Verification de l'existence du repertoire logs
if not exist logs (
    echo Creation du repertoire logs...
    mkdir logs
)

REM Execution du script Python
echo Execution du test de mise a jour par lots...
echo Les resultats seront enregistres dans logs/test_batch_update.log
echo.
python test_batch_update.py

echo.
echo Test termine.
echo Consultez le fichier logs/test_batch_update.log pour plus de details.

:end
echo.
pause
