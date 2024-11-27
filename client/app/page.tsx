import GitHubGlobe from '@/components/GitHubGlobe'
import Project from '@/components/Project'
import React from 'react'

export default function Home() {
  return (
    <section className='h-screen z-50 w-screen overflow-x-hidden overflow-y-auto relative'>
      <GitHubGlobe />
      <div className='h-screen w-screen grid place-content-center relative z-50'>
        <div id="header" className='w-max h-max flex flex-col justify-center items-center'>
          <h1 className='text-white text-5xl'>
            AI system for real-time Energy pricing
          </h1>
          <button className='bg-white rounded-md text-black px-2 py-1.5 mt-2'>Get Started</button>
        </div>
      </div>
      <Project />
    </section>
  )
}