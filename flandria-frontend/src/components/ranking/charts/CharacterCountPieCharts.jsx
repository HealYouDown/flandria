/* eslint-disable react/no-array-index-key */
import React from 'react';
import {
  Cell,
  Label,
  Legend,
  Pie, PieChart, ResponsiveContainer, Tooltip,
} from 'recharts';
import {
  bergruenColor, luxplenaColor, baseClasses, classnameToColor,
} from './constants';

const CharacterCountPieCharts = ({ data }) => {
  const totalCharacterData = [
    {
      key: 'bergruen',
      name: 'Bergruen',
      value: data.total_count_ber,
    },
    {
      key: 'luxplena',
      name: 'LuxPlena',
      value: data.total_count_lux,
    },
  ];

  const bergruenClassData = {
    base: [],
    cc: [],
  };

  const luxplenaClassData = {
    base: [],
    cc: [],
  };

  data.counts.forEach((entry) => {
    if (baseClasses.includes(entry.class.value)) {
      bergruenClassData.base.push({
        key: entry.class.value,
        name: entry.label,
        value: entry.Bergruen,
      });
      luxplenaClassData.base.push({
        key: entry.class.value,
        name: entry.label,
        value: entry.LuxPlena,
      });
    } else {
      bergruenClassData.cc.push({
        key: entry.class.value,
        name: entry.label,
        value: entry.Bergruen,
      });
      luxplenaClassData.cc.push({
        key: entry.class.value,
        name: entry.label,
        value: entry.LuxPlena,
      });
    }
  });

  return (
    <div className="flex flex-row justify-around">
      <ResponsiveContainer width="30%" height={500}>
        <PieChart>
          <Legend />
          <Tooltip />
          <Pie
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            paddingAngle={2}
            outerRadius={100}
            innerRadius={60}
            data={totalCharacterData}
            label
          >
            {totalCharacterData.map((entry) => (
              <Cell
                key={`cell-${entry.key}`}
                fill={entry.key === 'bergruen' ? bergruenColor : luxplenaColor}
              />
            ))}
            <Label position="center" value="Char count" />
          </Pie>
        </PieChart>
      </ResponsiveContainer>
      <ResponsiveContainer width="30%" height={500}>
        <PieChart>
          <Legend />
          <Tooltip />
          <Pie
            dataKey="value"
            nameKey="label"
            cx="50%"
            cy="50%"
            paddingAngle={2}
            outerRadius={100}
            innerRadius={60}
            data={bergruenClassData.base}
          >
            {bergruenClassData.base.map((entry) => (
              <Cell
                key={`cell-${entry.key}`}
                fill={classnameToColor[entry.key]}
              />
            ))}
            <Label position="center" value="Bergruen" />
          </Pie>
          <Pie
            dataKey="value"
            nameKey="label"
            cx="50%"
            cy="50%"
            paddingAngle={2}
            outerRadius={150}
            innerRadius={110}
            data={bergruenClassData.cc}
            label
          >
            {bergruenClassData.cc.map((entry) => (
              <Cell
                key={`cell-${entry.key}`}
                fill={classnameToColor[entry.key]}
              />
            ))}
          </Pie>
        </PieChart>
      </ResponsiveContainer>
      <ResponsiveContainer width="30%" height={500}>
        <PieChart>
          <Legend />
          <Tooltip />
          <Pie
            dataKey="value"
            nameKey="label"
            cx="50%"
            cy="50%"
            paddingAngle={2}
            outerRadius={100}
            innerRadius={60}
            data={luxplenaClassData.base}
          >
            {luxplenaClassData.base.map((entry) => (
              <Cell
                key={`cell-${entry.key}`}
                fill={classnameToColor[entry.key]}
              />
            ))}
            <Label position="center" value="LuxPlena" />
          </Pie>
          <Pie
            dataKey="value"
            nameKey="label"
            cx="50%"
            cy="50%"
            paddingAngle={2}
            outerRadius={150}
            innerRadius={110}
            data={luxplenaClassData.cc}
            isAnimationActive={false}
            label
          >
            {luxplenaClassData.cc.map((entry) => (
              <Cell
                key={`cell-${entry.key}`}
                fill={classnameToColor[entry.key]}
              />
            ))}
          </Pie>
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default CharacterCountPieCharts;
