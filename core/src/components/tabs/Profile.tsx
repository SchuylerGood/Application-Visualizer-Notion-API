export default function Profile(props: any) {
    return (
        <div className="w-full min-h-screen p-12 flex flex-col bg-white">
            <h1 className="text-3xl font-bold ml-4">Your Information</h1>
            <div className="flex flex-row w-full">
                <div className="flex-1 bg-gray-300 p-12 rounded-lg m-4">
                    <h1 className="text-2xl font-bold">Account Information</h1>
                    <div className="flex flex-row space-x-4">
                        <div className="flex flex-col space-y-2">
                            <p className="text-lg">Name:</p>
                            <p className="text-lg">Email:</p>
                            <p className="text-lg">Phone:</p>
                            <p className="text-lg">Location:</p>
                        </div>
                        <div className="flex flex-col space-y-2">
                            <p className="text-lg">{props.data.name}</p>
                            <p className="text-lg">{props.data.email}</p>
                            <p className="text-lg">{props.data.phone}</p>
                            <p className="text-lg">{props.data.location}</p>
                        </div>
                    </div>
                </div>

                <div className="flex-1 bg-gray-300 p-12 rounded-lg m-4">
                    <h1 className="text-2xl font-bold">Notion Database Information</h1>
                    <div className="flex flex-row space-x-4">
                        <div className="flex flex-col space-y-2">
                            <p className="text-lg ">Notion Token:</p>
                            <p className="text-lg ">Database ID:</p>
                        </div>
                        <div className="flex flex-col space-y-2">
                            <p className="text-lg">{props.data.notion_token}</p>
                            <p className="text-lg">{props.data.database_id}</p>
                        </div>
                    </div>
                </div>
            </div>
            
        </div>
    )
}