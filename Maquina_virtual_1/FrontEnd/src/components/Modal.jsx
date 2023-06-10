import { CloseOutlined } from '@ant-design/icons';
import { useRef } from 'react';


async function sendNewUrl (url){
  const newUrl = `https://${url}/`

  const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ link: newUrl })
  };

  try {
    const response = await fetch(`http://localhost:8000/api/links`, requestOptions);
    console.log("response: ", response);
  } catch (error) {
    console.log(error);
  }
}

export function Modal({ isOpen, onClose }) {
  const inputRef = useRef();

  if (!isOpen) {
    return null;
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    const newQuery = inputRef.current.value;
    console.log("newQuery:", newQuery);
    sendNewUrl(newQuery);
    onClose();
  }

  return (
    <div
      id="popup-modal"
      tabIndex="-1"
      className="fixed top-0 left-0 right-0 z-50 flex items-center justify-center w-full h-full p-4 overflow-x-hidden overflow-y-auto bg-gray-900 bg-opacity-50"
    >
      <div className="relative w-full max-w-md">
        <div className="relative bg-white rounded-lg shadow dark:bg-gray-700">
          <button
            type="button"
            className="absolute top-3 right-2.5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-gray-800 dark:hover:text-white"
            data-modal-hide="popup-modal"
            onClick={onClose}
          >
            <CloseOutlined />
          </button>
          <div className="p-6 text-center">
            <h3 className="mb-5 text-lg font-normal text-white">Agregar nueva url</h3>
            <form onSubmit={handleSubmit}>
              <input
                type="text"
                id="inputUrl"
                ref={inputRef}
                placeholder="www.google.com, www.twitch.tv, www.lun.com, etc..."
                className="w-full px-4 py-2 leading-tight text-gray-700 bg-gray-200 border-2 border-gray-200 rounded appearance-none focus:outline-none focus:bg-white focus:border-blue-800"
              />
              <div className="py-4">
                <button
                  data-modal-hide="popup-modal"
                  className="text-white bg-blue-600 hover:bg-blue-800 font-medium rounded-lg text-sm inline-flex items-center px-5 py-2.5 text-center mr-2"
                  type="submit"
                >
                  Enviar
                </button>
                <button
                  data-modal-hide="popup-modal"
                  type="button"
                  className="text-gray-500 bg-white hover:bg-gray-100 focus:ring-4 focus:outline-none focus:ring-gray-200 rounded-lg border border-gray-200 text-sm font-medium px-5 py-2.5 hover:text-gray-900 focus:z-10 dark:bg-gray-700 dark:text-gray-300 dark:border-gray-500 dark:hover:text-white dark:hover:bg-gray-600 dark:focus:ring-gray-600"
                  onClick={onClose}
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
