@echo off
REM Simple trace generator batch file
REM Usage: generate-trace.bat [pattern] [count]
REM Patterns: sequential, repeated, random, mixed
REM Default: sequential 1000

set pattern=%1
set count=%2

if "%pattern%"=="" set pattern=sequential
if "%count%"=="" set count=1000

echo Generating trace with %pattern% pattern, %count% accesses...

REM Create a temporary C# file and compile it
echo using System; > temp_trace_gen.cs
echo using System.IO; >> temp_trace_gen.cs
echo class TempTraceGen { >> temp_trace_gen.cs
echo     static void Main() { >> temp_trace_gen.cs
echo         Random rnd = new Random(); >> temp_trace_gen.cs
echo         using (StreamWriter sw = new StreamWriter("trace.txt")) { >> temp_trace_gen.cs

if "%pattern%"=="sequential" (
    echo             for (int i = 0; i ^^< %count%; i++) { >> temp_trace_gen.cs
    echo                 sw.WriteLine($"{l} 0x{i*4:X8} 4"); >> temp_trace_gen.cs
    echo             } >> temp_trace_gen.cs
) else if "%pattern%"=="repeated" (
    echo             int numAddresses = 16; >> temp_trace_gen.cs
    echo             for (int i = 0; i ^^< %count%; i++) { >> temp_trace_gen.cs
    echo                 int addr = (i %% numAddresses) * 4; >> temp_trace_gen.cs
    echo                 sw.WriteLine($"{l} 0x{addr:X8} 4"); >> temp_trace_gen.cs
    echo             } >> temp_trace_gen.cs
) else if "%pattern%"=="random" (
    echo             for (int i = 0; i ^^< %count%; i++) { >> temp_trace_gen.cs
    echo                 int addr = rnd.Next(0, 1024) * 4; >> temp_trace_gen.cs
    echo                 sw.WriteLine($"{l} 0x{addr:X8} 4"); >> temp_trace_gen.cs
    echo             } >> temp_trace_gen.cs
) else (
    echo             for (int i = 0; i ^^< %count%; i++) { >> temp_trace_gen.cs
    echo                 char op = (i %% 4 == 0) ? 's' : 'l'; >> temp_trace_gen.cs
    echo                 int addr = i * 4; >> temp_trace_gen.cs
    echo                 sw.WriteLine($"{op} 0x{addr:X8} 4"); >> temp_trace_gen.cs
    echo             } >> temp_trace_gen.cs
)

echo         } >> temp_trace_gen.cs
echo     } >> temp_trace_gen.cs
echo } >> temp_trace_gen.cs

csc temp_trace_gen.cs >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    temp_trace_gen.exe
    del temp_trace_gen.exe temp_trace_gen.cs
    echo Trace file generated successfully!
) else (
    echo Error: Could not compile trace generator. Make sure C# compiler is available.
    del temp_trace_gen.cs
    exit /b 1
)

