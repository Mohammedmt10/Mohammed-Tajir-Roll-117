import type { employeeCard } from './card';
import Card from './card';

interface IList {
    searchResult : employeeCard[]
}

export default function List(props : IList) {
    return <div className=''>
        {props.searchResult.length == 0 && <div className='text-center pt-8 text-xl'>
            No employee found.    
        </div>}
        {<div className='grid grid-cols-3 w-full pt-8 px-40 gap-4'>
            {props.searchResult.map((employee : employeeCard) => (
            <Card id={employee.id} name={employee.name} department={employee.department} designation={employee.designation} email={employee.email} date_of_joining={employee.date_of_joining} />
            ))}
        </div>}
    </div>
}