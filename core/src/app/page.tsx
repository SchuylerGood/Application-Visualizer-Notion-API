import Image from "next/image";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1 className="text-6xl font-bold">Welcome to my website</h1>
      <div className="flex flex-col items-center">
        <Image
          src="/images/profile.jpg"
          alt="Profile picture"
          width={200}
          height={200}
          className="rounded-full"
        />
        <h2 className="text-4xl font-bold mt-8">Hi, I'm John Doe</h2>
        <p className="text-2xl text-center mt-4">
          I'm a web developer and I love building websites and web applications.
        </p>
      </div>
    </main>
  );
}
