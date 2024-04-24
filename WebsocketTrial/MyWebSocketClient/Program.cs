using System;
using System.Net.WebSockets;
using System.Text;

class Program
{
    static async Task Main(string[] args)
    {
        using (ClientWebSocket ws = new ClientWebSocket())
        {
            Uri serverUri = new Uri("ws://localhost:8765/");
            await ws.ConnectAsync(serverUri, System.Threading.CancellationToken.None);
            Console.WriteLine("Connected to Python server!");

            Task sendTask = Task.Run(async () => await SendMessages(ws));
            Task receiveTask = Task.Run(async () => await ReceiveMessages(ws));

            await Task.WhenAll(receiveTask, sendTask);  // Ensuring all tasks are complete
        }
    }

    static async Task SendMessages(ClientWebSocket ws)
    {
        while (ws.State == WebSocketState.Open)
        {
            Console.Write("Enter message to send to Python: ");
            string? message = Console.ReadLine();
            if (!string.IsNullOrEmpty(message))
            {
                var buffer = Encoding.UTF8.GetBytes(message);
                await ws.SendAsync(new ArraySegment<byte>(buffer), WebSocketMessageType.Text, true, System.Threading.CancellationToken.None);
                Console.WriteLine("Message sent");
            }
        }
    }

    static async Task ReceiveMessages(ClientWebSocket ws)
    {
        Console.WriteLine("test");
        var buffer = new byte[1024];
        while (ws.State == WebSocketState.Open)
        {
            var result = await ws.ReceiveAsync(new ArraySegment<byte>(buffer), System.Threading.CancellationToken.None);
            if (result.MessageType == WebSocketMessageType.Text)
            {
                string message = Encoding.UTF8.GetString(buffer, 0, result.Count);
                Console.WriteLine($"Message from Python: {message}");
            }
            else if (result.MessageType == WebSocketMessageType.Close)
            {
                Console.WriteLine("Server has closed the connection");
                break;
            }
        }
    }
}


 