import { useState, useEffect } from 'react';
import './css/global.css';
import Decrypt from './Decrypt';
import Encrypt from "./Encrypt";
import Generate from "./Generate";

function App() {
  const [current, setCurrent] = useState("rsa");
  function clickHandler(alg){
    setCurrent(alg);
  }
  useEffect(() => {
    let mounted = true
    return () =>    { mounted = false  }
  }, [current])

  return (
    <div className="container">
      <div className="main-menu">
        <div className='box-bttn'>
          <div className='btn' type="submit"  >
            <span>Select Algorithm</span>
          </div>
          <div className='btn bttn submit ' type="submit" id="delimiter" value="rsa" onClick={() => clickHandler("rsa")}>
            <span>RSA</span>
          </div>
          <div className='btn bttn submit' type="submit" id="delimiter" value="ecc" onClick={() => clickHandler("ecc")}>
            <span>ECC</span>
          </div>
          <div className='btn' type="submit" >
            <span>Current Algorithm Used: {current}</span>
          </div>
        </div>
      </div>
      <div className="main-content">
        <Generate current={current}/>
        <Encrypt current={current}/>
        <Decrypt current={current}/>
      </div>
    </div>
  );
}

export default App;
