using System;
using System.Diagnostics;
using System.IO;

class RunExperiments
{
    static void Main()
    {
        string traceFile = "trace.txt";
        string resultsFile = "results.csv";
        
        // Check if trace file exists
        if (!File.Exists(traceFile))
        {
            Console.WriteLine($"Error: {traceFile} not found. Run GenerateTrace.cs first.");
            return;
        }
        
        // Header for CSV file
        using (StreamWriter sw = new StreamWriter(resultsFile))
        {
            sw.WriteLine("CacheSize,LineSize,Associativity,Policy,Hits,Accesses,HitRate");
            
            // Test different cache sizes (exponents: 8, 9, 10, 11)
            int[] cacheSizeExps = { 8, 9, 10, 11 };
            
            // Test different line sizes (exponents: 4, 5, 6)
            int[] lineSizeExps = { 4, 5, 6 };
            
            // Test different associativities
            string[] associativities = { "direct", "2way", "4way", "fully" };
            
            // Test both replacement policies
            string[] policies = { "lru", "fifo" };
            
            Console.WriteLine("Running cache simulation experiments...");
            Console.WriteLine("This may take a while...\n");
            
            int experimentCount = 0;
            int totalExperiments = cacheSizeExps.Length * lineSizeExps.Length * associativities.Length * policies.Length;
            
            foreach (int cacheSizeExp in cacheSizeExps)
            {
                foreach (int lineSizeExp in lineSizeExps)
                {
                    // Skip invalid combinations (line size can't be larger than cache size)
                    if (lineSizeExp >= cacheSizeExp)
                        continue;
                    
                    foreach (string associativity in associativities)
                    {
                        foreach (string policy in policies)
                        {
                            experimentCount++;
                            Console.Write($"Experiment {experimentCount}/{totalExperiments}: ");
                            Console.Write($"Cache={Math.Pow(2, cacheSizeExp)}B, ");
                            Console.Write($"Line={Math.Pow(2, lineSizeExp)}B, ");
                            Console.Write($"Assoc={associativity}, ");
                            Console.Write($"Policy={policy.ToUpper()}... ");
                            
                            try
                            {
                                // Run the simulator with command-line arguments
                                ProcessStartInfo psi = new ProcessStartInfo
                                {
                                    FileName = "dotnet",
                                    Arguments = $"run -- {cacheSizeExp} {lineSizeExp} {associativity} {policy} {traceFile}",
                                    RedirectStandardOutput = true,
                                    RedirectStandardError = true,
                                    UseShellExecute = false,
                                    CreateNoWindow = true
                                };
                                
                                using (Process process = Process.Start(psi))
                                {
                                    string output = process.StandardOutput.ReadToEnd();
                                    string error = process.StandardError.ReadToEnd();
                                    process.WaitForExit();
                                    
                                    if (process.ExitCode == 0 && !string.IsNullOrEmpty(output))
                                    {
                                        // Write the CSV line to results file
                                        sw.WriteLine(output.Trim());
                                        sw.Flush();
                                        Console.WriteLine("Done");
                                    }
                                    else
                                    {
                                        Console.WriteLine($"Error: {error}");
                                    }
                                }
                            }
                            catch (Exception ex)
                            {
                                Console.WriteLine($"Exception: {ex.Message}");
                            }
                        }
                    }
                }
            }
            
            Console.WriteLine($"\nExperiments complete! Results saved to {resultsFile}");
        }
    }
}

