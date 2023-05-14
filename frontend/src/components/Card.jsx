
import img from "../img/docIcon.jpg"

export function Card( {url, title, key, children} ){
    return(
        
        <div key={key} className="w-full max-w-sm transition duration-500 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700 hover:scale-110">
          <a href={url}>
            <img
              className="rounded-t-lg"
              src={img}
              alt="Imagen"
            />
          </a>
          <div className="p-5">
            <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
            {title}
            </h5>
            <p className="mb-3 font-normal text-gray-700 dark:text-gray-400">{children}</p>
          </div>
        </div>
        
    )

}