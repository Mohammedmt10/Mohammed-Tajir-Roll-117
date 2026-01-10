export default function InputBox(props : { setQuery : (value : string) => void}) {
    return <div className='mx-auto pt-6  flex justify-center w-96'>
      <input type="text" className='hover:border-blue-500 hover:scale-105 duration-400 border px-4 rounded-full py-2 outline-none w-full shadow-[0px_0px_10px_rgba(0,0,0,0.24)]' placeholder="Search by name" onChange={(e) => props.setQuery(e.target.value)} />
    </div>
}