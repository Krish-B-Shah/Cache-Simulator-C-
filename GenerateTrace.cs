using System;
using System.IO;

namespace TraceGenerator
{
    class Program
    {
        static void Main(string[] args)
    {
        string pattern = "sequential";
        int count = 1000;
        
        if (args.Length > 0)
            pattern = args[0].ToLower();
        if (args.Length > 1)
            count = int.Parse(args[1]);
        
        Random rnd = new Random();
        
        using (StreamWriter sw = new StreamWriter("trace.txt"))
        {
            switch (pattern)
            {
                case "sequential":
                    // Sequential accesses - good for testing spatial locality
                    for (int i = 0; i < count; i++)
                    {
                        sw.WriteLine($"l 0x{i*4:X8} 4");
                    }
                    break;
                    
                case "repeated":
                    // Repeated access to same addresses - good for testing temporal locality
                    int numAddresses = 16;
                    for (int i = 0; i < count; i++)
                    {
                        int addr = (i % numAddresses) * 4;
                        sw.WriteLine($"l 0x{addr:X8} 4");
                    }
                    break;
                    
                case "random":
                    // Random accesses - worst case scenario
                    for (int i = 0; i < count; i++)
                    {
                        int addr = rnd.Next(0, 1024) * 4; // Random addresses up to 4KB
                        sw.WriteLine($"l 0x{addr:X8} 4");
                    }
                    break;
                    
                case "mixed":
                    // Mix of loads and stores
                    for (int i = 0; i < count; i++)
                    {
                        char op = (i % 4 == 0) ? 's' : 'l'; // 25% stores, 75% loads
                        int addr = i * 4;
                        sw.WriteLine($"{op} 0x{addr:X8} 4");
                    }
                    break;
                    
                default:
                    Console.WriteLine("Unknown pattern. Using sequential.");
                    goto case "sequential";
            }
        }
        
        Console.WriteLine($"Generated trace.txt with {count} {pattern} memory accesses");
        }
    }
}
