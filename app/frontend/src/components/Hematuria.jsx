import { IoTriangle } from "react-icons/io5";

const Hematuria = () => {
  return (
    <div
      className="w-[750px] h-[136px] bg-red-300 rounded-xl 
                      shadow-xl flex flex-col justify-center items-center"
    >
      <div className="w-full flex justify-center gap-x-52">
        <div className="text-3xl font-bold text-slate-900">
          HEMATURIA SEVERITY
        </div>
        <div className="text-3xl text-slate-900">{50}% BLOOD</div>
      </div>
      <div className="w-5/6 h-20 flex justify-center items-center relative">
        <div className="w-full h-10 rounded-lg border-slate-200 border-x-8 border-y-4 flex flex-row">
          <div className="w-1/5 h-full bg-[#ddc588]"></div>
          <div className="w-1/5 h-full bg-[#cf8f70]"></div>
          <div className="w-1/5 h-full bg-[#a8372a]"></div>
          <div className="w-1/5 h-full bg-[#811e1b]"></div>
          <div className="w-1/5 h-full bg-[#491210]"></div>
        </div>

        <div
          className="w-10 h-full absolute transition-all duration-500 -translate-x-1/2 flex flex-col justify-between items-center"
          style={{ left: `50%` }}
        >
          <IoTriangle className="text-4xl text-slate-200 rotate-180" />
          <IoTriangle className="text-4xl text-slate-200" />
        </div>
      </div>
    </div>
  );
};

export default Hematuria;
