import { useEffect, useState } from 'react'
import './App.css'
import axios from 'axios';
import InputBox from './components/inputBox';
import NavBar from './components/navBar';
import type { employeeCard } from './components/card';
import List from './components/list';
import Footer from './components/footer';


function App() {

  const [loading , setLoading] = useState(true);
  const [query , setQuery] = useState("");
  const [search , setSearch] = useState("");
  const [searchResult , setSearchResult] = useState<employeeCard[]>([]);

  const fetchEmployee = async (query : string) => {
    const res = await axios.get(`http://127.0.0.1:8000/employees?search=${query}`)
    if(Array.isArray(res.data)) {
      setSearchResult(res.data);
    } else {
      setSearchResult([])
    }
    setLoading(false)
  }

  useEffect(() => {
    const timeout = setTimeout(() => {
      fetchEmployee(query)
    }, 500);
    return () => clearTimeout(timeout)
  }, [search]) 

  useEffect(() => {
    const timeout = setTimeout(() => {
      setSearch(query)
    }, 1000);
    return () => clearTimeout(timeout)
  }, [query]);

  if (loading) {
      return <div>
        loading...
    </div>
  }
  return <div className='h-screen'>
    <NavBar />
    <InputBox setQuery={setQuery} />
    <div className='h-full justify-between flex flex-col'>
      <List searchResult={searchResult} />
      <Footer />
    </div>
  </div>
}

export default App
