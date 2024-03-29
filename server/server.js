require('dotenv').config(); // Takes all env files into process.env

const express = require('express');
const notion = require('./notion');
const cors = require('cors'); // Import the cors middleware

const app = express();

app.use(cors({
    origin: 'http://localhost:3000'
}));

app.get('/', async (req, res) => {
    try {
        const data = await notion.readDatabase();
        let results = [];

        for (let i = 0; i < data.length; i++) {
            // Declare variables outside of try blocks
            let country = "";
            let city = "";
            let state = [];
            let simplify = false;
            let url = "";
            let status = [];
            let category = [];
            let company = "";
            let type = "";
            let title = "";

            // Country
            try {
                country = data[i]["properties"]["COUNTRY"]["select"]["name"];
            } catch (error) {}

            // City
            try {
                city = data[i]["properties"]["CITY"]["rich_text"][i]["text"]["content"];
            } catch (error) {}

            // State
            try {
                let states = data[i]["properties"]["STATE"]["multi_select"];
                states.forEach((item, index) => {
                    state.push(item["name"]);
                });
            } catch (error) {}

            // Simplify
            try {
                simplify = data[i]["properties"]["SIMPLIFY"]["checkbox"];
            } catch (error) {}

            // URL
            try {
                url = data[i]["properties"]["URL"]["url"];
            } catch (error) {}

            // STATUS
            try {
                let statuses = data[i]["properties"]["STATUS"]["multi_select"];
                statuses.forEach((item, index) => {
                    status.push(item["name"]);
                });
            } catch (error) {}

            // Category
            try {
                let categories = data[i]["properties"]["CATEGORY"]["multi_select"];
                categories.forEach((item, index) => {
                    category.push(item["name"]);
                });
            } catch (error) {}

            // Company
            try {
                company = data[i]["properties"]["COMPANY"]["rich_text"][i]["text"]["content"];
            } catch (error) {}

            // Type
            try {
                type = data[i]["properties"]["TYPE"]["select"]["name"];
            } catch (error) {}

            // Title
            try {
                title = data[i]["properties"]["TITLE"]["title"][i]["text"]["content"];
            } catch (error) {}

            // Push results to array
            results.push({
                "country": country,
                "city": city,
                "state": state,
                "simplify": simplify,
                "url": url,
                "status": status,
                "category": category,
                "company": company,
                "type": type,
                "title": title
            });
        }

        res.send(results);
    } catch (error) {
        console.error("Error:", error);
        res.send(error);
    }
});


// app.get('/api/data', async (req, res) => {
//     try{
//         const response = 
//     }
// })

app.listen(3001, () => {
    console.log('Server is running on port 3001');
});
