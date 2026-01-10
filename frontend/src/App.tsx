import { useEffect, useState } from 'react'
import './App.css'
import axios from 'axios';
import InputBox from './components/inputBox';
import NavBar from './components/navBar';
import type { employeeCard } from './components/card';
import List from './components/list';
import Footer from './components/footer';
import Loading from './components/loading';
import { http_url } from './config';


function App() {

  const [loading , setLoading] = useState(true);
  const [query , setQuery] = useState("");
  const [search , setSearch] = useState("");
  const [searchResult , setSearchResult] = useState<employeeCard[]>([]);

  const fetchEmployee = async (query : string) => {
    const res = await axios.get(`${http_url}/employees?search=${query}`)
    if(Array.isArray(res.data)) {
      setSearchResult(res.data);
    } else {
      setSearchResult([])
    }
    setLoading(false)
  }

  useEffect(() => { 
      fetchEmployee(query)
  }, [search]) 
  
  useEffect(() => {
    setLoading(true)
    const timeout = setTimeout(() => {
      setSearch(query)
    }, 500);
    return () => clearTimeout(timeout)
  }, [query]);

  return <div className='h-screen'>
    <NavBar />
    <InputBox setQuery={setQuery} />

    <div className='h-full'>
      {!loading && <div className='h-full flex justify-between flex-col'>
        <List searchResult={searchResult} />
        <Footer />
      </div>}
      {loading && <Loading />}
    </div> 
  </div>
}

export default App
