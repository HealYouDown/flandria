import { createBreakpoint, createMap } from "styled-components-breakpoint";

const breakpoints = {
  xs: 0,
  sm: 576,
  md: 768,
  lg: 992,
  xl: 1200,
};
 
const breakpoint = createBreakpoint(breakpoints);
const map = createMap(breakpoints);
export default breakpoint;
export {
  map
}