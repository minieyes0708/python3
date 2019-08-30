FOR /F "usebackq delims=|" %%f IN (`dir /b ^| findstr /i MI_INDEX_2019`) DO (
	DEL %%f
)
