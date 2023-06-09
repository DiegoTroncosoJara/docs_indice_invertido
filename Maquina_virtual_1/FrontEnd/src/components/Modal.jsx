import { CloseOutlined  } from '@ant-design/icons';

export function Modal({ isOpen, onClose }) {
  if (!isOpen) {
    return null;
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
          <h3 className="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">
            Agregar nueva url
          </h3>
          <input type="text"  className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500" id="inline-full-name" type="text" value="Jane Doe"/>
          <div className='py-4'>

            <button
              data-modal-hide="popup-modal"
              type="button"
              className="text-white bg-red-600 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 dark:focus:ring-red-800 font-medium rounded-lg text-sm inline-flex items-center px-5 py-2.5 text-center mr-2"
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
        </div>
      </div>
    </div>
  </div>
  );
}
