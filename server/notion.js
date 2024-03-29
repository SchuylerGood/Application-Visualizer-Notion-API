// All notion related code

const { Client } = require("@notionhq/client");

const notion = new Client({ auth: process.env.NOTION_TOKEN });


// Use this to get your database proporty ID's
// async function getDatabase() {
//     const response = await notion.databases.retrieve({
//         database_id: process.env.DATABASE_ID
//     })
//     console.log(response["properties"])
// }

// getDatabase()

async function readDatabase() {
    try {
        const response = await notion.databases.query({
            database_id: process.env.DATABASE_ID,
        });

        // Extracting the results
        const results = response.results;

        return results

    } catch (error) {
        console.error("Error:", error.body);
    }
}

// (async () => {
//     const results = await readDatabase();
//     console.log(results[0]); // Modify this as per your data structure
// })();

module.exports = { readDatabase }