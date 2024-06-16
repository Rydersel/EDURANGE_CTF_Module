import {env} from "process";

export default async function handler(req, res) {
    if (req.method === 'POST') {
        const { command } = req.body;

        const response = await fetch(`${env.IP}/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ command }),
        });

        const data = await response.json();
        res.status(response.status).json(data);
    } else {
        res.status(405).end();
    }
}
