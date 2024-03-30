import { useState } from "react";

type SideBarProps = {
    onTabChange: (tab: string) => void;
  };

export default function SideBar({ onTabChange }: SideBarProps) {


    const [currentTab, setCurrentTab] = useState("Home");

    // Function to handle tab change
    const handleTabChange = (tab: string) => {
        setCurrentTab(tab);
        // Call the function passed from the parent component
        if (onTabChange) {
            onTabChange(tab);
        }
    };

    return (
        <div className="w-96 h-full bg-gray-200 p-4">
            <div className="flex flex-col justify-center bg-white w-full h-40 px-8 py-4 rounded-lg border-2 shadow-black opacity-100 ">
                <h1 className="text-5xl font-bold">Job Hunt</h1>
                <h3 className="text-2xl">Dashboard</h3>
            </div>
            <div className="flex flex-col items-start space-y-3 py-4">
                <button 
                    className="
                        flex items-start bg-gray-200 w-full px-8 py-4 rounded-lg 
                        transition-all duration-300 hover:bg-white
                    "
                    onClick={() => handleTabChange("Home")}
                >
                    <img
                        className="w-8 h-8"
                        src="icons/B_House.svg"
                        alt="Home Icon"
                    />
                    <h2 className="text-2xl font-medium ml-4">Home</h2>
                </button>
                <button 
                    className="
                        flex items-start bg-gray-200 w-full px-8 py-4 rounded-lg 
                        transition-all duration-300 hover:bg-white
                    "
                    onClick={() => handleTabChange("Graphs")}
                >
                    <img
                        className="w-8 h-8"
                        src="icons/B_Graph.svg"
                        alt="Graphs Icon"
                    />
                    <h2 className="text-2xl font-medium ml-4">Graphs</h2>
                </button>
                <button 
                    className="
                        flex items-start bg-gray-200 w-full px-8 py-4 rounded-lg 
                        transition-all duration-300 hover:bg-white
                    "
                    onClick={() => handleTabChange("Profile")}
                >
                    <img
                        className="w-8 h-8"
                        src="icons/B_Profile.svg"
                        alt="Profile Icon"
                    />
                    <h2 className="text-2xl font-medium ml-4">Profile</h2>
                </button>
                <button 
                    className="
                        flex items-start bg-gray-200 w-full px-8 py-4 rounded-lg 
                        transition-all duration-300 hover:bg-white
                    "
                    onClick={() => handleTabChange("Settings")}
                >
                    <img
                        className="w-8 h-8"
                        src="icons/B_Settings.svg"
                        alt="Settings Icon"
                    />
                    <h2 className="text-2xl font-medium ml-4">Settings</h2>
                </button>
            </div>
        </div>
    )
}