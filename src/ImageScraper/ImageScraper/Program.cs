using Google.Apis.Customsearch.v1;
using Google.Apis.Customsearch.v1.Data;
using Google.Apis.Services;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Net;
using System.Runtime.InteropServices;

namespace ImageScraper
{
    class Program
    {
        const string apiKey = "AIzaSyAm3u3lVtBxF2YGOhzy-d4lOM6xSMUZJOU";
        const string searchEngineId = "013458683623921094043:oapf1u1prax";
        const string trainingPath = "./images/training/";
        const string testingPath = "./images/testing/";
        static void Main(string[] args)
        {
            //Console.WriteLine("Hello World!");

            var startPage = 0;
            var count = 0;
            var query = "";

            Console.WriteLine("Enter query:");
            query = Console.ReadLine();

            Console.WriteLine("Enter the starting page");
            startPage = Convert.ToInt32(Console.ReadLine());

            Console.WriteLine("Enter the number of pages to read (each page is 10 results)");
            count = Convert.ToInt32(Console.ReadLine());

            Search(query, startPage, count);

            return;

        }

        public static void VerifySaveDirectory(string tag)
        {
            System.IO.Directory.CreateDirectory("./"+tag);
        }


        public static void Search(string query, int start, int count)
        {
            if (query==null || query == "")
            {
                Console.WriteLine("Please enter a valid query");
                return;
            }

            if (start < 0)
            {
                Console.WriteLine("Please enter a non-negative start page value");
                return;
            }

            if (count < 1)
            {
                Console.WriteLine("Please enter a positive count page value");
                return;
            }

            VerifySaveDirectory($@"{trainingPath}{query}");
            VerifySaveDirectory($@"{testingPath}{query}");

            var searchService = new CustomsearchService(new BaseClientService.Initializer {ApiKey=apiKey });
            var listRequest = searchService.Cse.List(query);
            listRequest.Cx = searchEngineId;


            var paging = new List<Result>();
            var page = start;

            var imageResult = new List<Result.ImageData>();

            //Analytics
            int totalResults = 0;

            while (paging != null)
            {
                if (page >= count + start)
                {
                    Console.WriteLine("End paging.");
                    break;
                }

                Console.WriteLine($"Page {page-start} of {count}");
                listRequest.Start = page * 10 + 1;
                listRequest.Num = 10;
                listRequest.FileType = "png jpg jpeg";
                listRequest.SearchType = CseResource.ListRequest.SearchTypeEnum.Image;
                //listRequest.ImgType = CseResource.ListRequest.ImgTypeEnum.Photo;
                
                paging = (List<Result>) listRequest.Execute().Items;
                ++page;
                if (paging == null) { continue; }

                totalResults += paging.Count;

                foreach(var item in paging)
                {
                    Console.WriteLine(item.Link);

                    if (item.Image != null)
                    {
                        imageResult.Add(item.Image);
                        Console.WriteLine($"Image found! {item.Title}");

                        using (WebClient client = new WebClient())
                        {
                            byte[] data = client.DownloadData(item.Link);

                            using (MemoryStream mem = new MemoryStream(data)){
                                using (var image = Image.FromStream(mem))
                                {
                                    var r = new Random();
                                    string name = "";

                                    if (totalResults % 9 == 0)
                                    {
                                        name = $@"{testingPath}{query}/image_{r.Next(10000, Int32.MaxValue)}.jpg";
                                    } else
                                    {
                                        name = $@"{trainingPath}{query}/image_{r.Next(10000, Int32.MaxValue)}.jpg";
                                    }

                                    image.Save(name, ImageFormat.Jpeg);
                                }
                                
                            }
                            /*
                            Stream stream = client.OpenRead(item.Link);
                            Bitmap bitmap = new Bitmap(stream);
                            

                            if (bitmap == null)
                            {
                                Console.WriteLine("Failed to convert file");
                            }
                            else
                            {
                                try
                                {
                                    bitmap.Save($@"{trainingPath}{query}/{item.Title}.png", ImageFormat.Png);
                                } catch(ExternalException e)
                                {
                                    Console.WriteLine("External exception");
                                } catch (Exception e)
                                {
                                    Console.WriteLine(e.InnerException);
                                }
                                
                                Console.WriteLine("Done!");

                            }

                            stream.Flush();
                            stream.Close();
                            client.Dispose();*/
                        }

                    } else
                    {
                        Console.WriteLine($"Item rejected : {item.Title}");
                    }
                 
                }
            }

            if (totalResults != 0)
            {
                float percentImage = ((float)imageResult.Count / (float)totalResults) * 100;
                Console.WriteLine($"{totalResults} results : {Environment.NewLine} {percentImage}% images");
                Console.WriteLine($"Downloading {query} images");

                
            } else
            {
                Console.WriteLine("No results");
                return;
            }
            
        }
    }
}
