import { useState } from 'react'
import Head from 'next/head'
import ChatInterface from '@/components/ChatInterface'

export default function Home() {
  return (
    <>
      <Head>
        <title>LLM for SE - Code Generation Agent</title>
        <meta name="description" content="AI-powered code generation assistant" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className="h-screen bg-chat-bg">
        <ChatInterface />
      </main>
    </>
  )
}
