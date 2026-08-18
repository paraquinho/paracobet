export const impliedProbability = (decimalOdds: number) => {
  if (decimalOdds <= 1) throw new Error("Decimal odds must exceed 1");
  return 1 / decimalOdds;
};
export const calculateEdge = (modelProbability: number, decimalOdds: number) => modelProbability - impliedProbability(decimalOdds);
