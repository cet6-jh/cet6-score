@echo off
chcp 65001 >nul
REM ============================================
REM CET6 链接续期脚本
REM 功能：自动更新过期时间戳到 30 分钟后，并推送到 GitHub Pages
REM 用法：双击运行 refresh-deploy.bat
REM ============================================

setlocal

cd /d "%~dp0"

echo.
echo ==========================================
echo   CET6 链接续期部署脚本
echo   当前时间：%date% %time%
echo ==========================================
echo.

REM 1. 计算新的过期时间戳（30分钟后）
for /f "delims=" %%t in ('python -c "import time; t=int(time.time())+1800; print(t)"') do set EXPIRE_TS=%%t

echo [1/5] 新过期时间戳：%EXPIRE_TS%
echo       对应时间：%EXPIRE_TS% 秒（请手动转北京时间查看）
echo.

REM 2. 用 Python 修改 index.html 中的过期时间戳
echo [2/5] 修改 index.html 中的过期时间戳...
python update_expire.py %EXPIRE_TS%
if errorlevel 1 (
    echo       错误：修改失败！请检查 Python 是否安装。
    pause
    exit /b 1
)
echo       完成
echo.

REM 3. git 提交
echo [3/5] git add + commit...
git add index.html
git commit -m "chore: 续期链接（30分钟有效）%EXPIRE_TS%"
if errorlevel 1 (
    echo       警告：commit 失败（可能没有改动），继续推送
)
echo.

REM 4. git push
echo [4/5] git push origin main...
git push origin main
if errorlevel 1 (
    echo       错误：推送失败！请检查网络/GitHub 认证
    pause
    exit /b 1
)
echo       完成
echo.

REM 5. 等待 Pages 构建 + 输出新地址
echo [5/5] 等待 GitHub Pages 构建（约 30 秒）...
timeout /t 30 /nobreak >nul

echo.
echo ==========================================
echo   ✅ 部署完成！
echo   新过期时间戳：%EXPIRE_TS%
echo   公网地址：https://cet6-jh.github.io/cet6-score/
echo   （约 1 分钟后可正常访问）
echo ==========================================
echo.
echo 按任意键重新生成二维码...
pause >nul
python generate_qrcode.py
echo.
echo 完成！二维码已更新到 qrcode.png 和 qrcode-share.png
pause