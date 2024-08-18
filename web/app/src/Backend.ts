export class Backend {
    private readonly backendUrl: string;

    constructor(backendUrl: string) {
        this.backendUrl = backendUrl;
    }

    async startDebate()  {
        let endpoint: string = this.backendUrl + "/start-debate"
        try {
            const response = await fetch(endpoint);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json(); // Parse the JSON
            // Access the 'message' property from the response
            const message = data.message;
            return message; // Return the message or use it as needed
        } catch (error) {
            console.error('Failed to fetch:', error);
            throw error; // Re-throw error if you want to handle it further up the call stack
        }
    }
}

export {}
