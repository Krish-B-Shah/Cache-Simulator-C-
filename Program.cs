using System;
using System.Collections.Generic;
using System.IO;

namespace CacheSimulator
{
    class Program
    {
        static string GetBinary(char hex)
        {
            if (hex == '0')
                return "0000";
            if (hex == '1')
                return "0001";
            if (hex == '2')
                return "0010";
            if (hex == '3')
                return "0011";
            if (hex == '4')
                return "0100";
            if (hex == '5')
                return "0101";
            if (hex == '6')
                return "0110";
            if (hex == '7')
                return "0111";
            if (hex == '8')
                return "1000";
            if (hex == '9')
                return "1001";
            if ((hex == 'a') || (hex == 'A'))
                return "1010";
            if ((hex == 'b') || (hex == 'B'))
                return "1011";
            if ((hex == 'c') || (hex == 'C'))
                return "1100";
            if ((hex == 'd') || (hex == 'D'))
                return "1101";
            if ((hex == 'e') || (hex == 'E'))
                return "1110";
            if ((hex == 'f') || (hex == 'F'))
                return "1111";
            return "";
        }

        static int GetTag(string addr, int tagSize)
        {
            string tagBinary = "";
            int tag = 0;
            string extra;
            int numHex = tagSize / 4;
            int numExtra = tagSize % 4;
            int i;

            for (i = 0; i < numHex; i++)
                tagBinary += GetBinary(addr[i + 2]);

            if (numExtra > 0)
            {
                extra = GetBinary(addr[i + 2]);
                for (int j = 0; j < numExtra; j++)
                    tagBinary += extra[j];
            }

            int multiplier = 1;
            for (i = tagSize - 1; i >= 0; i--)
            {
                if (tagBinary[i] == '1')
                    tag += multiplier;
                multiplier *= 2;
            }

            return tag;
        }

        static int GetSet(string addr, int tagsize, int setsize)
        {
            int set = 0;
            string binaryAddress = "";
            string setBinary = "";

            for (int i = 0; i < 8; i++)
                binaryAddress += GetBinary(addr[i + 2]);

            for (int i = 0; i < setsize; i++)
                setBinary += binaryAddress[tagsize + i];

            //now turn setBinary into decimal
            int multiplier = 1;
            for (int i = setsize - 1; i >= 0; i--)
            {
                if (setBinary[i] == '1')
                    set += multiplier;
                multiplier *= 2;
            }

            return set;
        }

        static bool CheckCache(int set, int setSizeExp, List<List<int>> cache, int tag, int counter, int lru)
        {
            if (setSizeExp == 0) //direct mapped
            {
                if (cache[set][0] == tag)
                {
                    cache[set][1] = counter;
                    return true;
                }
                else
                {
                    cache[set][0] = tag;
                    cache[set][1] = counter;
                    return false;
                }
            }

            double setSize = Math.Pow(2, setSizeExp);
            int j = set * (int)setSize;
            int emptySpot = -1;
            int smallestCounter = -1;
            int lineToReplace = -1;

            for (int i = 0; i < setSize; i++)
            {
                if (cache[i + j][0] == tag)
                {
                    if (lru == 1)
                        cache[i + j][1] = counter;
                    return true;
                }
                else if (cache[i + j][0] == -1)
                {
                    emptySpot = i + j;
                }
                else if (smallestCounter == -1)
                {
                    smallestCounter = cache[i + j][1];
                    lineToReplace = i + j;
                }
                else if (cache[i + j][1] < smallestCounter)
                {
                    smallestCounter = cache[i + j][1];
                    lineToReplace = i + j;
                }
            }

            //empty spot?
            if (emptySpot != -1) //there was an empty spot, fill it
            {
                cache[emptySpot][0] = tag;
                cache[emptySpot][1] = counter;
            }
            else //update entry with lowest counter
            {
                cache[lineToReplace][0] = tag;
                cache[lineToReplace][1] = counter;
            }

            return false;
        }

        static void Main(string[] args)
        {
            int cacheSizeExp;
            int lru = 0;
            int lineSizeExp;
            int setSizeExp;
            string filename;
            int numLinesExp;
            bool autoMode = args.Length >= 5;

            if (autoMode)
            {
                // Command-line mode: cacheSizeExp lineSizeExp associativity policy filename
                // associativity: "direct", "2way", "4way", "8way", "16way", "fully"
                // policy: "lru" or "fifo"
                cacheSizeExp = int.Parse(args[0]);
                lineSizeExp = int.Parse(args[1]);
                string associativity = args[2].ToLower();
                string policy = args[3].ToLower();
                filename = args[4];
                
                numLinesExp = cacheSizeExp - lineSizeExp;
                
                // Determine setSizeExp from associativity
                if (associativity == "fully")
                    setSizeExp = numLinesExp;
                else if (associativity == "direct")
                    setSizeExp = 0;
                else if (associativity == "2way")
                    setSizeExp = 1;
                else if (associativity == "4way")
                    setSizeExp = 2;
                else if (associativity == "8way")
                    setSizeExp = 3;
                else if (associativity == "16way")
                    setSizeExp = 4;
                else
                {
                    Console.WriteLine($"Unknown associativity: {associativity}");
                    return;
                }
                
                lru = (policy == "lru") ? 1 : 0;
            }
            else
            {
                // Interactive mode
                Console.WriteLine("This is a rudimentary cache simulator. It is your responsibility to ensure that the parameters you enter make sense");
                Console.WriteLine("Cache size is an exponent of 2. E.g. if the exponent is 3, the cache is 2 to the 3, or 8 bytes");
                Console.WriteLine("Enter the exponent for the cache size");
                cacheSizeExp = int.Parse(Console.ReadLine());

                Console.WriteLine("Line size is an exponent of 2. E.g. if the exponent is 3, the cache is 2 to the 3, or 8 bytes");
                Console.WriteLine("Enter the exponent for the line size");
                lineSizeExp = int.Parse(Console.ReadLine());

                numLinesExp = cacheSizeExp - lineSizeExp;
                //numLines = 2^numLinesExp

                char fa, dm, lru_char;

                Console.WriteLine("Is the cache fully associative? Enter 'Y' or 'y' if yes, any other character if no");
                fa = Console.ReadLine()[0];

                if ((fa == 'y') || (fa == 'Y'))
                    setSizeExp = numLinesExp;
                else
                {
                    Console.WriteLine("Is the cache direct mapped? Enter 'Y' or 'y' if yes, any other character if no");
                    dm = Console.ReadLine()[0];

                    if ((dm == 'y') || (dm == 'Y'))
                        setSizeExp = 0;
                    else
                    {
                        Console.WriteLine("Enter '1' for 2 lines per set, '2' for 4 lines per set, '3' for 8 lines per set, or '4' for 16 lines per set.");
                        setSizeExp = int.Parse(Console.ReadLine());

                        if ((setSizeExp > 4) || (setSizeExp < 1))
                        {
                            Console.WriteLine("Try again. It's your responsibility to enter numbers that make sense");
                            return;
                        }
                    }
                }

                Console.WriteLine("What is the replacement policy? L or l for LRU, anything else for FIFO");
                lru_char = Console.ReadLine()[0];

                if ((lru_char == 'l') || (lru_char == 'L'))
                    lru = 1;

                Console.WriteLine("Enter filename");
                filename = Console.ReadLine();
            }
            int numSetsExp = numLinesExp - setSizeExp; //set field size
            //zero for fully associative

            int tagsize = 32 - numSetsExp - lineSizeExp;
            int numLines = (int)Math.Pow(2, numLinesExp);

            List<List<int>> cache = new List<List<int>>();
            for (int i = 0; i < numLines; i++)
            {
                //each line has three parameters: tag, set, access time
                //set all to -1 to start
                cache.Add(new List<int> { -1, -1 }); //tag, access counter
            }

            using (StreamReader newfile = new StreamReader(filename))
            {
                string line;
                int counter = 0;
                bool hit;
                int numhits = 0;

                while ((line = newfile.ReadLine()) != null)
                {
                    string[] parts = line.Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
                    if (parts.Length < 2)
                        continue;

                    string ls = parts[0];
                    string addr = parts[1];

                    int tag = GetTag(addr, tagsize);
                    int set;

                    if (numSetsExp == 0)
                        //if numSetsExp=0, then number of sets = 1 (2^0=1), and it is fully associative
                        //there is only one set
                        set = 0;
                    else
                        set = GetSet(addr, tagsize, numSetsExp);

                    //check for hit or miss
                    if (CheckCache(set, setSizeExp, cache, tag, counter, lru))
                    {
                        numhits++;
                    }

                    counter++;
                }

                float hitrate = (float)numhits / (float)counter;
                
                if (autoMode)
                {
                    // CSV format for automation: CacheSize,LineSize,Associativity,Policy,Hits,Accesses,HitRate
                    int cacheSize = (int)Math.Pow(2, cacheSizeExp);
                    int lineSize = (int)Math.Pow(2, lineSizeExp);
                    string associativity = (setSizeExp == 0) ? "direct" : 
                                         (setSizeExp == numLinesExp) ? "fully" : 
                                         $"{Math.Pow(2, setSizeExp)}way";
                    string policy = (lru == 1) ? "LRU" : "FIFO";
                    Console.WriteLine($"{cacheSize},{lineSize},{associativity},{policy},{numhits},{counter},{hitrate:F4}");
                }
                else
                {
                    Console.WriteLine($"Hits {numhits} accesses {counter} hit rate {hitrate}");
                }
            }
        }
    }
}

