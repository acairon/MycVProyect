@echo off

for %%F in (*.md) do (
    pandoc "%%F" -o "%%~nF.docx"
)