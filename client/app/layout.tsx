import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Comfortaa } from "next/font/google";

const comfortaa = Comfortaa({
  subsets: ['cyrillic'],
  weight: '500'
})


export const metadata: Metadata = {
  title: "Energy Price",
  description: "Final year project of Batch 34",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`bg-black dark ${comfortaa.className} `}>{children}</body>
    </html>
  );
}
