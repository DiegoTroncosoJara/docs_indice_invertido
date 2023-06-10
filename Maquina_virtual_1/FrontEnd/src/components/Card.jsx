import img from "../img/docIcon.jpg";

export function Card({ url, title, children }) {
  return (
    <div className="w-full max-w-sm transition duration-500 border border-gray-900 rounded-3xl bg-slate-100 hover:scale-110">
      <a href={url}>
        <img className="rounded-t-lg" src={img} alt="Imagen" />
      </a>
      <div className="p-5">
        <h5 className="mb-2 overflow-hidden text-2xl font-bold tracking-tight text-gray-900 truncate">
          {title}
        </h5>
        <p className="mb-3 font-normal text-gray-700 ">
          {children}
        </p>
      </div>
    </div>


  
  )
}
