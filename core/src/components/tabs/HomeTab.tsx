import BarChart from "@/components/BarChart";
import DoughnutChart from "@/components/DoughnutChart";

function processData(data: any) {
    let numbers: {[key: string] : number} = {};
    if (data) {
        for (let i = 0; i < data.length; i++) {
            let statuses = data[i].status;
            statuses.forEach((status: string) => {
                if(
                    status !== "Interview 1 -> Scheduled" && 
                    status !== "Interview 2 -> Scheduled" && 
                    status !== "Interview 3 -> Scheduled" && 
                    status !== "Tech Assessment -> Scheduled" &&
                    status !== "Coffee Chat" &&
                    status !== "Referral"
                ) {
                    if (!numbers.hasOwnProperty(status)) {
                        numbers[status] = 1;
                    } else {
                        numbers[status] += 1;
                    }
                }
            });
        }
    }

    let labels = Object.keys(numbers);
    let values = Object.values(numbers);

    for (let i = 0; i < labels.length; i++) {        
        if (labels[i] === "Tech Assessment -> Complete") {
            labels[i] = "Tech Assessment";
        } else if (labels[i] === "Interview 1 -> Complete") {
            labels[i] = "Interview 1";
        } else if (labels[i] === "Interview 2 -> Complete") {
            labels[i] = "Interview 2";
        } else if (labels[i] === "Interview 3 -> Complete") {
            labels[i] = "Interview 3";
        } else if (labels[i] === "Need to Apply") {
            labels[i] = "Added";
        }
    }

    return [labels, values]
}

export default function HomeTab(props: any) {
    let labels = processData(props.data)[0];
    let values = processData(props.data)[1];

    return (
        <div className="w-full h-full m-12 flex flex-col mt-44">
            <div>
                <h1 className="text-3xl font-bold">Welcome Back, John</h1>
                <p>Welcome to your Dashboard home page! You can find all your analytics and insights here on how your job search is going</p>
            </div>
            <div className="flex flex-row space-x-2 my-8">
                <button 
                    className="flex flex-row items-center space-x-2 py-4 px-5 bg-blue-700 text-white font-bold rounded-lg"
                >
                    <img
                        src="icons/W_Refresh.svg"
                        alt="Refresh Icon"
                        className="w-8 h-8"
                    ></img>
                    <p>Refresh Data</p>
                </button>
                <a 
                    href="https://www.notion.so/40f9b23ad53148289bd97288a5e51544?v=5865b913d43a4293aff578a0d0ee264f" 
                    className="flex flex-row items-center space-x-2 py-4 px-5 bg-blue-700 text-white font-bold rounded-lg"
                >
                    <img
                        src="icons/W_Plus.svg"
                        alt="Refresh Icon"
                        className="w-8 h-8"
                    ></img>
                    <p>Add Data</p>
                </a>
            </div>
            <div className="flex flex-row space-x-8">
                <div className="bg-gray-200 flex flex-col w-fit rounded-lg p-8 border">
                    <h1 className="text-4xl font-bold mb-1">Jobs Applied</h1>
                    <BarChart labels={labels.slice(0,4)} values={values.slice(0,4)}/>
                </div>
                <div className="bg-gray-200 flex flex-col w-fit rounded-lg p-8 border">
                    <h1 className="text-4xl font-bold mb-1">Interviews</h1>
                    <BarChart labels={labels.slice(4,7)} values={values.slice(4,7)}/>
                </div>
            </div>
        </div>
    );
}