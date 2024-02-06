import SupplyVolume from "./SupplyVolume";
import SupplyRate from "./SupplyRate";

const Supply = () => {
  return (
    <div className="w-full h-[158px] flex flex-row justify-between items-center">
      <SupplyVolume />
      <SupplyRate />
    </div>
  );
};

export default Supply;
