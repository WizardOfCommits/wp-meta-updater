@echo off
echo Test de l'API Rank Math SEO
echo ========================
echo.

set /p site_url=URL du site WordPress (ex: https://1min30.com): 
set /p post_id=ID de l'article a tester: 
set /p username=Nom d'utilisateur WordPress: 
set /p password=Mot de passe ou jeton: 

echo.
echo Execution du test...
echo.

python test_rank_math_seo.py "%site_url%" %post_id% "%username%" "%password%"

echo.
pause
