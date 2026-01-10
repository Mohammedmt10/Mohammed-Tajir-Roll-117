export interface employeeCard {
  id : number,
  name : string,
  department : string,
  designation : string,
  email : string,
  date_of_joining : string
}
export default function Card(props : employeeCard) {
    return <div key={props.id} className="border-2 cursor-pointer hover:scale-105 duration-200 w-full border-neutral-400 text-center px-10 rounded mx-4 py-4 bg-white shadow-[0px_0px_10px_rgba(0,0,0,0.25)]">
        <div className="text-lg font-semibold">
            {props.name}
        </div>
        <div className="underline">
            {props.email}
        </div>
        <div>
           Department: {props.department}
        </div>
        <div>
           Designation {props.designation}
        </div>
        <div>
            Joined : {props.date_of_joining}
        </div>
    </div>
}