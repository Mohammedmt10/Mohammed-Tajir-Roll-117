export default  function NavBar() {
    return <div className="flex justify-between px-10 bg-white py-4 border-b-neutral-500 border-b-2">
        <div className="text-2xl font-bold cursor-pointer">
            Smart Works
        </div>

        <div className="flex gap-4 text-xl cursor-pointer">
            <div className="hover:bg-black hover:text-white rounded duration-200 p-1 px-3">
                Home
            </div>
            <div className="hover:bg-black hover:text-white rounded duration-200 p-1 px-3">
                Employees
            </div>
            <div className="hover:bg-black hover:text-white rounded duration-200 p-1 px-3">
                About
            </div>
        </div>
    </div>
}