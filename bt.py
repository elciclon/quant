import bt

data = bt.get(
    "ypf,ypfd.ba,ggal,ggal.ba,bma,bma.ba,pam,pamp.ba,bbar,bbar.ba", start="2000-7-25"
)

print(data.head())

data["ccl"] = (
    data["ggalba"] / data["ggal"] * 10
    + data["bmaba"] / data["bma"] * 10
    + data["ypfdba"] / data["ypf"]
    + data["pampba"] / data["pam"] * 25
    + data["bbarba"] / data["bbar"] * 3
) / 5


with open("ccl_data.csv", "w") as f:
    data.to_csv(f)

print(data.tail())
