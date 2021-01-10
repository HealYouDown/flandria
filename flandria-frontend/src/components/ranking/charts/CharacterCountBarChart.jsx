import React from 'react';
import {
  Bar,
  BarChart, CartesianGrid, Label, LabelList, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from 'recharts';
import { bergruenColor, classnameOrderValue, luxplenaColor } from './constants';

const CharacterCountBarChart = ({ data }) => (
  <ResponsiveContainer width="100%" height={600}>
    <BarChart
      data={data.sort(
        (a, b) => classnameOrderValue[a.class.value] > classnameOrderValue[b.class.value],
      )}
      margin={{
        bottom: 20,
      }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="label">
        <Label position="insideTop" offset={30} value="Class count for each Server" />
      </XAxis>
      <YAxis />
      <Legend verticalAlign="middle" layout="vertical" align="right" />
      <Tooltip />
      <Bar dataKey="Bergruen" fill={bergruenColor}>
        <LabelList dataKey="Bergruen" position="top" />
      </Bar>
      <Bar dataKey="LuxPlena" fill={luxplenaColor}>
        <LabelList dataKey="LuxPlena" position="top" />
      </Bar>
    </BarChart>
  </ResponsiveContainer>
);

export default CharacterCountBarChart;
