import React, { useRef, useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { solid } from '@fortawesome/fontawesome-svg-core/import.macro'
import { getImage, ImageType } from './utils/api';

const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d')!;

function App() {
  const imRef = useRef<HTMLImageElement>(null);
  const dataUrl = useRef<string>('');
  const [imageType, setImageType] = useState(ImageType.Montage);

  const onClick = (type = imageType) => {
    if (!imRef.current) return;
    imRef.current.src = getImage(type);
    console.log(imRef.current.src)
  }

  const onImgLoad = () => {
    if (!imRef.current) return;
    canvas.height = imRef.current.naturalHeight;
    canvas.width = imRef.current.naturalWidth;
    ctx.drawImage(imRef.current, 0, 0);
    dataUrl.current = canvas.toDataURL('png');
  }

  const onShareClick = () => {
    const contentType = 'image/png';
    const byteCharacters = atob(dataUrl.current.substring(`data:${contentType};base64,`.length));
    const byteArrays = [];
    for (let offset = 0; offset < byteCharacters.length; offset += 1024) {
      const slice = byteCharacters.slice(offset, offset + 1024);

      const byteNumbers = new Array(slice.length);
      for (let i = 0; i < slice.length; i++) {
        byteNumbers[i] = slice.charCodeAt(i);
      }

      const byteArray = new Uint8Array(byteNumbers);

      byteArrays.push(byteArray);
    }
    const blob = new Blob(byteArrays, { type: contentType });
    const blobUrl = URL.createObjectURL(blob);

    window.open(blobUrl, '_blank');
  }

  return (
    <div className="text-white h-screen w-screen overflow-hidden bg-gray-900 p-4 flex flex-col justify-center md:text-xl text-base ">
      <div className='mx-auto my-2 object-contain p-4 bg-gray-800 rounded-lg flex flex-col' >
        <img ref={imRef} src={getImage(imageType)} className='object-contain rounded-lg' onLoad={onImgLoad} />
        <div className="flex flex-col md:flex-row w-full justify-center md:space-x-4">
          <label className="relative flex justify-between items-center group p-2">
            Choose Similar Faces
            <input
              checked={imageType === ImageType.Similar}
              type="checkbox"
              className="absolute left-1/2 -translate-x-1/2 w-full h-full peer appearance-none rounded-md"
              onChange={() => {
                setImageType(imageType === ImageType.Montage ? ImageType.Similar : ImageType.Montage);
                onClick(imageType === ImageType.Montage ? ImageType.Similar : ImageType.Montage);
              }} />
            <span className="w-16 h-10 flex items-center flex-shrink-0 ml-4 p-1 bg-gray-300 rounded-full duration-300 ease-in-out peer-checked:bg-green-400 after:w-8 after:h-8 after:bg-white after:rounded-full after:shadow-md after:duration-300 peer-checked:after:translate-x-6 group-hover:after:translate-x-1"></span>
          </label>

          <button
            className='bg-green-500 rounded px-4 py-3 mt-4  text-white w-full'
            onClick={() => onClick()}>
            Randomize
          </button>

          <button
            className='bg-blue-500 rounded px-6 py-3 mt-4  text-white'
            onClick={onShareClick}>
            <FontAwesomeIcon icon={solid('share-from-square')} />
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
