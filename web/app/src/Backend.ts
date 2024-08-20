import {DebateInfo} from "./App"

export class Backend {
    private readonly backendUrl: string;

    constructor(backendUrl: string) {
        this.backendUrl = backendUrl;
    }


    async startDebate(debateInfo: DebateInfo)  {
        let endpoint: string = this.backendUrl + "/start-debate"
        try {
            const response = await fetch(
                endpoint,
                {
                    method: 'POST',
                    body: JSON.stringify({
                        "topic": debateInfo.getStartingPrompt()
                    }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

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

    async sendFiles(fileContents: string, isDebaterA: boolean){
        // Append each file to the FormData object
        console.log(fileContents);
        let fp: FilePayload = new FilePayload(fileContents, isDebaterA)

        try {
            const response = await fetch(this.backendUrl + "/input-files", {
                method: 'POST',
                body: JSON.stringify(fp),
                headers: {
                    'Content-Type': 'application/json'
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const result = await response.json();
            console.log('Success:', result);
        } catch (error) {
            console.error('Error:', error);
        }
    }
}

class FilePayload{
    public file_contents: string;
    public is_debater_a: boolean;

    constructor(fileContent: string, isDebaterA: boolean) {
        this.file_contents = fileContent;
        this.is_debater_a = isDebaterA;
    }
}

export {}