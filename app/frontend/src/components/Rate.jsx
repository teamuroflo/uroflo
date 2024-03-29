import SupplyRate from "./SupplyRate";
import WasteRate from "./WasteRate";

const Rate = () => {
  return (
    <div className="w-full h-[162px] flex flex-row justify-between items-center">
      <SupplyRate />
      <WasteRate />
    </div>
  );
};

export default Rate;
