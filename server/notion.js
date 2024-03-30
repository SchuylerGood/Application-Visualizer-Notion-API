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

// async function readDatabase() {
//     try {
//         const response = await notion.databases.query({
//             database_id: process.env.DATABASE_ID,
//         });

//         // Extracting the results
//         console.log(response.has_more);
//         console.log(response.next_cursor);
//         const results = response.results;

//         return results

//     } catch (error) {
//         console.error("Error:", error.body);
//     }
    
// }

async function readDatabase() {
    let resultsArr = [];
    let hasMore = true;
    let nextCursor = null;

    // First page
    try {
        const response = await notion.databases.query({
            database_id: process.env.DATABASE_ID,
        });

        // Extracting the results
        // console.log(response.has_more);
        // console.log(response.next_cursor);
        const results = response.results;
        hasMore = response.has_more;
        nextCursor = response.next_cursor;
        resultsArr = resultsArr.concat(response.results)
    } catch (error) {
        console.error("Error:", error.body);
    }

    // Next pages
    try {
        
        

        while (hasMore) {
            const response = await notion.databases.query({
                database_id: process.env.DATABASE_ID,
                start_cursor: nextCursor
            });

            // Concatenate the results
            resultsArr = resultsArr.concat(response.results);

            // Update hasMore and nextCursor for pagination
            hasMore = response.has_more;
            nextCursor = response.next_cursor;
        }

        return resultsArr;
    } catch (error) {
        console.error("Error:", error.body);
    }
}


module.exports = { readDatabase }

    // data = self.databases.query(databaseID)
    // database_object = data['object']
    // has_more = data['has_more']
    // next_cursor = data['next_cursor']
    // while has_more == True:
    //     data_while = self.databases.query(databaseID, start_cursor=next_cursor)
    //     for row in data_while['results']:
    //         data['results'].append(row)
    //     has_more = data_while['has_more']
    //     next_cursor = data_while['next_cursor']

    // new_database = {
    //     "object": database_object,
    //     "results": data["results"],
    //     "next_cursor": next_cursor,
    //     "has_more": has_more
    // }
    // return new_database