
REM create requirements.txt 
REM NOTE: on windows % is escaped using %%
REM =======================================
echo # requirements > requirements.txt
echo hivemind @ git+https://github.com/eelcovanvliet/hivemind.git@master >> requirements.txt
echo OrcFxAPI >> requirements.txt
echo scipy >> requirements.txt
echo pytest >> requirements.txt


REM inplace environment creation
REM =======================================
call conda remove --prefix ./.venv --all -y
call conda create --prefix ./.venv -y
call activate ./.venv
call conda install pip -y
call pip install -r requirements.txt

REM git init
REM echo *.txt > .gitignore
REM git submodule add 


cmd /k