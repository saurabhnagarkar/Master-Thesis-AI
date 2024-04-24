using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

class Program
{
    static void Main()
    {
        Thread serverThread = new Thread(new ThreadStart(CreateServer));
        serverThread.Start();

        // Example sending a message to Python
        SendMessageToPython("Hello from C#!");
    }

    static void CreateServer()
    {
        var listener = new TcpListener(IPAddress.Parse("127.0.0.1"), 6500);
        listener.Start();
        Console.WriteLine("C# server listening on port 6500...");

        while (true)
        {
            var client = listener.AcceptTcpClient();
            var thread = new Thread(HandleClient);
            thread.Start(client);
        }
    }

    static void HandleClient(object obj)
    {
        var client = (TcpClient)obj;
        var stream = client.GetStream();
        byte[] buffer = new byte[1024];
        int bytes;
        while ((bytes = stream.Read(buffer, 0, buffer.Length)) != 0)
        {
            var data = Encoding.UTF8.GetString(buffer, 0, bytes);
            Console.WriteLine("Received from Python: " + data);
        }
    }

    static void SendMessageToPython(string message)
    {
        using (var client = new TcpClient("127.0.0.1", 6000))
        using (var stream = client.GetStream())
        {
            byte[] data = Encoding.UTF8.GetBytes(message);
            stream.Write(data, 0, data.Length);
        }
    }
}
